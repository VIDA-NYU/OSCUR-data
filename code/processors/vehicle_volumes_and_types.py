#!/usr/bin/env python3
"""
Vehicle Volumes & Types | Merge Processor
────────────────────────────────────────────────────────────
Goal:
1) Attach street geometry (the_geom) to Vehicle Classification Counts by joining
   SegmentID (classification) ↔ PHYSICALID (centerline).
2) Snap ATR (Automated Traffic Volume Counts) point records to the nearest
   centerline to assign a PHYSICALID.
3) Output a single, location-aware long-form CSV.

Run:
python -m code.processors.vehicle_volumes_and_types.merge_counts_with_centerline \
  --classification data/vehicle_volumes_and_types/vehicle_classification_counts_2011_2024.csv \
  --centerline    data/vehicle_volumes_and_types/nyc_street_centerline.csv \
  --atr           data/vehicle_volumes_and_types/automated_traffic_volume_counts.csv \
  --out           data/vehicle_volumes_and_types/vehicle_counts_merged.csv
"""

from pathlib import Path
import argparse
import re
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
from shapely.geometry import Point

# CRS
CRS_WGS84  = "EPSG:4326"
CRS_METRIC = "EPSG:2263"   # NAD83 / New York Long Island (ftUS)

# ─────────────────────────  loaders  ─────────────────────────

def _parse_wkt_series(s: pd.Series):
    """Parse WKT if present (tolerant to None/NaN)."""
    return s.apply(lambda x: loads(x) if isinstance(x, str) and re.search(r"[A-Z]+\s*\(", x) else None)

def load_centerline(path: Path) -> gpd.GeoDataFrame:
    df = pd.read_csv(path, low_memory=False)

    # Ensure columns exist
    if "the_geom" not in df.columns:
        raise ValueError("Centerline file missing 'the_geom' column.")
    if "PHYSICALID" not in df.columns:
        cand = next((c for c in df.columns if c.lower() == "physicalid"), None)
        if not cand:
            raise ValueError("Centerline file missing 'PHYSICALID' column.")
        df.rename(columns={cand: "PHYSICALID"}, inplace=True)

    # Clean PHYSICALID like "46,810" → 46810
    df["PHYSICALID"] = (
        df["PHYSICALID"].astype(str).str.replace(",", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
        .astype("Int64")
    )

    # Parse WKT MULTILINESTRING/LINESTRING; centerline is in WGS84 on NYC Open Data
    geom = df["the_geom"].apply(lambda s: loads(str(s)) if isinstance(s, str) else None)
    gdf = gpd.GeoDataFrame(df, geometry=geom, crs=CRS_WGS84).dropna(subset=["geometry"]).to_crs(CRS_METRIC)

    keep_cols = ["PHYSICALID", "the_geom"]
    extra_ids = [c for c in df.columns if c.endswith("ID") and c != "PHYSICALID"]
    return gdf[["geometry"] + list(dict.fromkeys(keep_cols + extra_ids))]


def load_classification(path: Path) -> pd.DataFrame:
    """Vehicle Classification Counts (2011–2024). Must contain SegmentID."""
    df = pd.read_csv(path, low_memory=False)
    # Normalize column name to 'SegmentID'
    if "SegmentID" not in df.columns:
        candidates = [c for c in df.columns if c.lower() == "segmentid"]
        if candidates:
            df.rename(columns={candidates[0]: "SegmentID"}, inplace=True)
        else:
            raise ValueError("Classification file missing 'SegmentID' column.")

    # standardize dtypes that often cause join misses
    df["SegmentID"] = pd.to_numeric(df["SegmentID"], errors="coerce").astype("Int64")
    return df

def load_atr(path: Path) -> gpd.GeoDataFrame:
    """
    Load ATR counts. Handles:
    - WKT in 'WktGeom' (NYSP ftUS, EPSG:2263)
    - WKT in 'the_geom' (WGS84)
    - numeric lon/lat fallbacks
    """
    df = pd.read_csv(path, low_memory=False)

    # column aliases
    wktgeom_col = next((c for c in df.columns if c.lower() == "wktgeom"), None)
    thegeom_col = next((c for c in df.columns if c.lower() == "the_geom"), None)

    if wktgeom_col and df[wktgeom_col].astype(str).str.contains("POINT", na=False).any():
        # ATR: WktGeom is in EPSG:2263 (values like 991497, 1229579.5)
        geom = df[wktgeom_col].apply(lambda s: loads(str(s)) if isinstance(s, str) else None)
        gdf = gpd.GeoDataFrame(df, geometry=geom, crs=CRS_METRIC).dropna(subset=["geometry"])
        return gdf  # already in metric CRS

    if thegeom_col and df[thegeom_col].astype(str).str.contains("POINT", na=False).any():
        # If an export has WGS84 the_geom
        geom = df[thegeom_col].apply(lambda s: loads(str(s)) if isinstance(s, str) else None)
        gdf = gpd.GeoDataFrame(df, geometry=geom, crs=CRS_WGS84).dropna(subset=["geometry"]).to_crs(CRS_METRIC)
        return gdf

    # numeric lon/lat fallbacks
    lon_candidates = [c for c in df.columns if c.upper() in {"LON","LONG","LONGITUDE","POINT_X","X"}]
    lat_candidates = [c for c in df.columns if c.upper() in {"LAT","LATITUDE","POINT_Y","Y"}]
    if lon_candidates and lat_candidates:
        lon = pd.to_numeric(df[lon_candidates[0]], errors="coerce")
        lat = pd.to_numeric(df[lat_candidates[0]], errors="coerce")
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(lon, lat), crs=CRS_WGS84).dropna(subset=["geometry"]).to_crs(CRS_METRIC)
        return gdf

    raise ValueError("ATR file missing parsable geometry (no 'WktGeom'/'the_geom' POINT or lon/lat columns).")


# ────────────────────────  processing  ───────────────────────

def join_classification_to_centerline(class_df: pd.DataFrame,
                                      center_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Join classification rows to centerline by SegmentID ↔ PHYSICALID.
    Keep the line geometry, and compute lon/lat from a representative point
    (so we never call .x/.y on line geometries).
    """
    # 0) dtype hygiene
    left = class_df.copy()
    left["SegmentID"] = pd.to_numeric(left["SegmentID"], errors="coerce").astype("Int64")

    # 1) fast ID index merge
    id_index = center_gdf[["PHYSICALID"]].copy()
    id_index["__row__"] = id_index.index
    out = left.merge(id_index, how="left", left_on="SegmentID", right_on="PHYSICALID")

    # 2) attach line geometry from center_gdf where matched
    geom = [None] * len(out)
    sel = out["__row__"].notna()
    if sel.any():
        geom_vals = center_gdf.loc[out.loc[sel, "__row__"].astype(int), "geometry"].values
        for i, g in zip(out.index[sel], geom_vals):
            geom[i] = g

    # 3) construct GeoDataFrame with active geometry set (no warning)
    gdf = gpd.GeoDataFrame(out.drop(columns=["__row__"]), geometry=gpd.GeoSeries(geom, crs=CRS_METRIC))

    # 4) export helpers:
    #    - WKT of the *line* in WGS84
    #    - lon/lat from a representative point of the line (always valid)
    gdf_wgs_lines = gdf.geometry.to_crs(CRS_WGS84)
    gdf["geom_wkt"] = gdf_wgs_lines.apply(lambda g: g.wkt if g is not None else None)

    rep_pts = gdf_wgs_lines.representative_point()
    gdf["lon"] = rep_pts.x.where(gdf.geometry.notna(), None)
    gdf["lat"] = rep_pts.y.where(gdf.geometry.notna(), None)

    gdf["source"] = "classification"
    return gdf


def snap_atr_to_centerline(atr_gdf: gpd.GeoDataFrame, center_gdf: gpd.GeoDataFrame, max_ft: int = 120) -> gpd.GeoDataFrame:
    """Nearest-line match to assign PHYSICALID to ATR points."""
    joined = gpd.sjoin_nearest(
        atr_gdf,
        center_gdf[["geometry", "PHYSICALID"]],
        how="left",
        max_distance=max_ft,
        distance_col="dist_to_centerline_ft",
    ).drop(columns=["index_right"])

    # Export helpful WGS84 fields
    out = joined.copy()
    out["lon"] = out.geometry.to_crs(CRS_WGS84).x
    out["lat"] = out.geometry.to_crs(CRS_WGS84).y
    out["geom_wkt"] = out.geometry.to_crs(CRS_WGS84).apply(lambda g: g.wkt if g is not None else None)
    out["source"] = "atr"
    return out

def standardize_for_union(df: pd.DataFrame, id_col: str = "PHYSICALID") -> pd.DataFrame:
    """
    Create a minimal common schema to union the two datasets.
    Keep identifiers, datetime if present, any count/volume columns, and location fields.
    """
    cols = list(df.columns)

    # Try to detect a timestamp column
    time_cols_pref = [c for c in cols if re.search(r"(date|time|timestamp)", c, re.I)]
    time_col = time_cols_pref[0] if time_cols_pref else None

    # Try to detect obvious count columns
    count_like = [c for c in cols if re.search(r"(count|volume|veh|trucks|cars|total)", c, re.I)]

    keep = [c for c in [id_col, "SegmentID", time_col, "lon", "lat", "geom_wkt", "source"] if c and c in cols]
    # Add a handful of count measures
    keep_extra = [c for c in count_like if c not in keep]
    keep = list(dict.fromkeys(keep + keep_extra))
    return df[keep].copy()

# ───────────────────────────  main  ────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Merge Vehicle Classification & ATR counts with Centerline geometry")
    ap.add_argument("--classification", required=True, type=Path, help="CSV – Vehicle Classification Counts (2011–2024)")
    ap.add_argument("--centerline",    required=True, type=Path, help="CSV – NYC Street Centerline (with the_geom WKT)")
    ap.add_argument("--atr",           required=True, type=Path, help="CSV – Automated Traffic Volume Counts (ATR)")
    ap.add_argument("--out",           required=True, type=Path, help="Output CSV for merged long-form dataset")
    args = ap.parse_args()

    # Load sources
    center = load_centerline(args.centerline)
    class_df = load_classification(args.classification)
    atr_gdf  = load_atr(args.atr)

    # 1) Classification: SegmentID ↔ PHYSICALID
    class_joined = join_classification_to_centerline(class_df, center)

    # 2) ATR: snap to centerline (nearest)
    atr_joined = snap_atr_to_centerline(atr_gdf, center, max_ft=120)

    # 3) Union with a common schema
    class_std = standardize_for_union(class_joined)
    atr_std   = standardize_for_union(atr_joined)

    merged = pd.concat([class_std, atr_std], ignore_index=True)

    # Save
    args.out.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(args.out, index=False)

    print(f"✅ Saved merged dataset: {len(merged):,} rows → {args.out}")
    print(f"   Classification rows: {len(class_std):,}")
    print(f"   ATR rows           : {len(atr_std):,}")
    print("   Schema:", list(merged.columns))

if __name__ == "__main__":
    main()
