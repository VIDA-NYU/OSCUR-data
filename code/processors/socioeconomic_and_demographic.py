"""
Processor | Socioeconomic & Demographic (ACS NTA Profiles) → Wide + Merged

One script does it all:
- Accepts either RAW cross-tab ACS CSVs (headers like 'Estimate' blocks) or already
  tidy long CSVs (columns: NTA, Indicator, Estimate). Auto-detects which.
- Converts (if needed) raw cross-tabs → long → wide with source prefixes:
    demo__*, econ__*, housing__*, socio__*
- Splits NTA into code + name, merges all sources by NTA, and attaches lon/lat
  from the NTA geometry CSV (kyz5-72x5) by name.

Run example (using your raw files and NTA geometry CSV):
python -m code.processors.socioeconomic_and_demographic \
  --demo    data/socioeconomic_and_demographic/nta_profiles/acs_demo_08to12_ntas.csv \
  --econ    data/socioeconomic_and_demographic/nta_profiles/acs_select_econ_08to12_ntas.csv \
  --housing data/socioeconomic_and_demographic/nta_profiles/acs_select_housing_08to12_ntas.csv \
  --socio   data/socioeconomic_and_demographic/nta_profiles/acs_socio_08to12_ntas.csv \
  --nta_geo data/socioeconomic_and_demographic/nta_population.csv \
  --out     data/socioeconomic_and_demographic/acs_nta_all_wide.csv
"""

from __future__ import annotations

from pathlib import Path
import argparse
import re
import pandas as pd
import geopandas as gpd
from shapely import wkt

def _slug(s: str) -> str:
    s = str(s)
    s = re.sub(r"\s+", "_", s.strip())
    s = re.sub(r"[^0-9A-Za-z_]+", "", s)
    return s.lower()

def _split_nta(nta: pd.Series) -> pd.DataFrame:
    """Split 'BK72 Williamsburg' → code='BK72', name='Williamsburg'. Robust to missing code."""
    nta = nta.fillna("").astype(str).str.strip()
    m = nta.str.extract(r"^(?P<nta_code>[A-Z]{2}\d{2})\s+(?P<nta_name>.+)$")
    out = pd.DataFrame({
        "NTA_full": nta,
        "NTA_code": m["nta_code"].where(m["nta_code"].notna(), None),
        "NTA_name": m["nta_name"].where(m["nta_name"].notna(), nta),
    })
    out["NTA_name_key"] = (
        out["NTA_name"].astype(str)
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    return out

def _looks_like_long(df: pd.DataFrame) -> bool:
    cols = {c.lower() for c in df.columns}
    return {"nta", "indicator", "estimate"}.issubset(cols)

def _parse_crosstab_csv(csv_path: str) -> pd.DataFrame:
    """
    Read a RAW cross-tab CSV (multi-column blocks with 'Estimate' headers)
    and return a tidy long DataFrame: NTA | Indicator | Estimate
    """
    raw = pd.read_csv(csv_path, header=None, dtype=str, keep_default_na=False)
    header_slice = raw.head(25)

    est_positions = []
    for r in header_slice.index:
        for c in header_slice.columns:
            if header_slice.iat[r, c].strip().lower() == "estimate":
                est_positions.append((r, c))
    if not est_positions:
        raise ValueError(f"No 'Estimate' header found in {csv_path}")

    est_cols = []
    col_to_geo = {}
    seen = set()
    for r, c in est_positions:
        # geography name usually the row above (sometimes two above)
        geo = header_slice.iat[max(r - 1, 0), c].strip()
        if not geo:
            geo = header_slice.iat[max(r - 2, 0), c].strip()
        if c not in seen:
            est_cols.append(c)
            col_to_geo[c] = geo
            seen.add(c)

    # first non-empty indicator row after banner text
    indicators = raw.iloc[:, 0].astype(str).str.strip()
    start_row = 0
    for i, val in indicators.items():
        if i > 5 and val not in ("", "nan", "None"):
            start_row = i
            break

    keep_mask = indicators.ne("").values
    keep_mask[:start_row] = False

    frames = []
    for c in est_cols:
        nta = col_to_geo.get(c, "").strip()
        vals = raw.iloc[:, c].astype(str).str.strip()
        df = pd.DataFrame(
            {"NTA": nta, "Indicator": indicators, "Estimate": vals}
        )
        df = df[keep_mask & df["Estimate"].ne("") & df["Estimate"].ne("-")]
        df["Estimate"] = pd.to_numeric(df["Estimate"], errors="coerce")
        df = df[df["Indicator"].ne("") & df["Estimate"].notna()]
        if not df.empty:
            frames.append(df)

    if not frames:
        raise ValueError(f"Parsed zero rows from {csv_path}")
    out = pd.concat(frames, ignore_index=True)
    out["Indicator"] = out["Indicator"].str.replace(r"\s+", " ", regex=True).str.strip()
    out["NTA"] = out["NTA"].str.replace(r"\s+", " ", regex=True).str.strip()
    return out[["NTA", "Indicator", "Estimate"]]

def _load_long_or_raw(path: str) -> pd.DataFrame:
    """Return a tidy long DF (NTA | Indicator | Estimate) from either raw cross-tab or long CSV."""
    df = pd.read_csv(path)
    if _looks_like_long(df):
        # Normalize column names just in case
        ren = {c: c.strip().title() for c in df.columns}
        df = df.rename(columns=ren)
        # Ensure exact names
        df = df.rename(columns={"Nta": "NTA", "Indicator": "Indicator", "Estimate": "Estimate"})
        return df[["NTA", "Indicator", "Estimate"]]
    # raw cross-tab → parse
    return _parse_crosstab_csv(path)

def _pivot_wide(long_df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    keys = _split_nta(long_df["NTA"])
    df = pd.concat(
        [keys[["NTA_full", "NTA_code", "NTA_name", "NTA_name_key"]],
         long_df.drop(columns=["NTA"]).reset_index(drop=True)],
        axis=1
    )
    df["col"] = prefix + "__" + df["Indicator"].map(_slug)
    wide = (
        df.pivot_table(
            index=["NTA_full", "NTA_code", "NTA_name", "NTA_name_key"],
            columns="col", values="Estimate", aggfunc="first"
        ).reset_index()
    )
    wide.columns.name = None
    return wide

def _load_nta_geo(nta_geo_csv: str) -> pd.DataFrame:
    """
    Read NTA geometry CSV and return polygons keyed by code.
    Must contain:
      - 'the_geom' (WKT MULTIPOLYGON)
      - 'nta2020' or 'nta2010' or 'ntacode'
    """
    gdf = pd.read_csv(nta_geo_csv)

    # --- pick code column ---
    code_cols = ["nta2020", "nta2010", "ntacode", "NTA2020", "NTA2010"]
    code_col = next((c for c in code_cols if c in gdf.columns), None)
    if not code_col:
        raise ValueError(
            "NTA geo CSV must contain one of these code columns: " + ", ".join(code_cols)
        )

    # --- geometry column ---
    geom_col = "the_geom"
    if geom_col not in gdf.columns:
        raise ValueError("NTA geo CSV must contain 'the_geom' column (WKT polygons).")

    out = gdf[[code_col, geom_col]].copy()
    out = out.rename(columns={code_col: "NTA_code"})
    return out.drop_duplicates("NTA_code")

def _order_columns(df: pd.DataFrame) -> pd.DataFrame:
    ident = [c for c in ["NTA_full","NTA_code","NTA_name","the_geom"] if c in df.columns]
    demo = sorted([c for c in df.columns if c.startswith("demo__")])
    econ = sorted([c for c in df.columns if c.startswith("econ__")])
    house = sorted([c for c in df.columns if c.startswith("housing__")])
    socio = sorted([c for c in df.columns if c.startswith("socio__")])
    other = [c for c in df.columns if c not in ident + demo + econ + house + socio]
    return df[ident + demo + econ + house + socio + other]

# ------------------------------- main ----------------------------------------

def main():
    ap = argparse.ArgumentParser(description="ACS NTA profiles → wide + merged with coordinates (single-step).")
    ap.add_argument("--demo",    required=True, help="Demographics CSV (raw cross-tab or long).")
    ap.add_argument("--econ",    required=True, help="Economic CSV (raw cross-tab or long).")
    ap.add_argument("--housing", required=True, help="Housing CSV (raw cross-tab or long).")
    ap.add_argument("--socio",   required=True, help="Social characteristics CSV (raw cross-tab or long).")
    ap.add_argument("--nta_geo", required=True, help="NTA geometry CSV (kyz5-72x5) with the_geom & ntaname2020.")
    ap.add_argument("--out",     required=True, help="Output merged wide CSV.")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print("• Reading/normalizing inputs (auto-detecting RAW vs LONG)…")
    demo_long  = _load_long_or_raw(args.demo)
    econ_long  = _load_long_or_raw(args.econ)
    house_long = _load_long_or_raw(args.housing)
    socio_long = _load_long_or_raw(args.socio)

    print("• Pivoting each to wide with grouped prefixes…")
    demo_w  = _pivot_wide(demo_long,  "demo")
    econ_w  = _pivot_wide(econ_long,  "econ")
    house_w = _pivot_wide(house_long, "housing")
    socio_w = _pivot_wide(socio_long, "socio")

    print("• Merging the four wide tables by NTA…")
    merged = demo_w.merge(econ_w,  on=["NTA_full","NTA_code","NTA_name","NTA_name_key"], how="outer")
    merged = merged.merge(house_w, on=["NTA_full","NTA_code","NTA_name","NTA_name_key"], how="outer")
    merged = merged.merge(socio_w, on=["NTA_full","NTA_code","NTA_name","NTA_name_key"], how="outer")

    print("• Attaching polygons from NTA geometry (code-based join)…")
    geo = _load_nta_geo(args.nta_geo)
    merged = merged.merge(geo, on="NTA_code", how="left")

    merged = _order_columns(merged).drop(columns=["NTA_name_key"], errors="ignore")

    merged.to_csv(out_path, index=False)
    print(f"✔ Saved merged wide file → {out_path}  rows={len(merged):,}  cols={len(merged.columns):,}")

if __name__ == "__main__":
    main()