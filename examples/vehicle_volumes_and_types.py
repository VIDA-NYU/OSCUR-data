#!/usr/bin/env python3
"""
Vehicle Volumes & Types | Full Processor (merge + aggregations)

Inputs
------
--classification : NYC DOT Vehicle Classification Counts (2011–2024) CSV
                   (wide-by-time with columns like 'Veh Class Type' and '12:00 AM', '12:15 AM', ...)
--atr            : NYC DOT Automated Traffic Volume Counts CSV
                   (POINT geometry in WKT (WktGeom/the_geom) or lon/lat)
--centerline     : NYC Street Centerline CSV (must contain 'PHYSICALID' and 'the_geom' WKT)
--out            : Output CSV

What it does
------------
1) Load & clean centerline geometry (WKT → GeoDataFrame @ EPSG:2263).
2) Parse the classification file (melt all time-of-day columns), bucket classes
   (cars / trucks / buses / bikes), aggregate to SegmentID (+Date), and attach
   centerline geometry by SegmentID ↔ PHYSICALID.
3) Snap ATR points to nearest centerline (sjoin_nearest) with a max distance
   (default 120 ft) and aggregate volumes by PHYSICALID.
4) Combine per-segment metrics and export:
   - class totals and buckets (cars / trucks / buses / bikes)
   - ATR total sum, mean, and sample count (days/records)
   - geometry WKT + representative lon/lat for quick mapping

Note on spatial merge
---------------------
ATR records are point samples; we assign them to the *nearest* centerline segment
within a configurable buffer (`--snap-ft`, default 120 ft). This is implemented
with GeoPandas `sjoin_nearest` after projecting to EPSG:2263 (feet). If a point
is farther than the threshold, it remains unmatched.

Run
---
python -m code.processors.vehicle_volumes_and_types \
  --classification data/vehicle_volumes_and_types/vehicle_classification_counts_2011_2024.csv \
  --atr           data/vehicle_volumes_and_types/automated_traffic_volume_counts.csv \
  --centerline    data/vehicle_volumes_and_types/nyc_street_centerline.csv \
  --out           data/vehicle_volumes_and_types/vehicle_counts_merged.csv
"""

from pathlib import Path
import argparse
import re
import pandas as pd
import geopandas as gpd
from typing import Optional
from shapely.wkt import loads as wkt_loads

CRS_WGS84  = "EPSG:4326"
CRS_METRIC = "EPSG:2263"  # ftUS (NY Long Island)

# ----------------------- helpers -----------------------

def _coerce_int(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype("Int64")

def _parse_wkt_if_present(s: pd.Series):
    return s.apply(lambda v: wkt_loads(str(v)) if isinstance(v, str) and "(" in v else None)

# Vehicle-class bucketing for the classification file
CLASS_BUCKET_MAP = {
    # cars
    "auto": "cars",
    "taxis": "cars",
    "passenger": "cars",

    # trucks
    "commercial": "trucks",
    "medium truck": "trucks",
    "heavy truck": "trucks",
    "box truck": "trucks",
    "single unit truck": "trucks",
    "combination truck": "trucks",

    # buses
    "school bus": "buses",
    "other bus": "buses",
    "bus": "buses",

    # bikes
    "bicycle": "bikes",
    "bike": "bikes",
}

TIME_COL_REGEX = re.compile(r"^\s*(\d{1,2}):(\d{2})\s*(AM|PM)\s*$", re.I)

# ----------------------- loaders -----------------------

def load_centerline(path: Path) -> gpd.GeoDataFrame:
    df = pd.read_csv(path, low_memory=False)

    # Normalize PHYSICALID
    if "PHYSICALID" not in df.columns:
        cand = next((c for c in df.columns if c.lower() == "physicalid"), None)
        if not cand:
            raise ValueError("Centerline missing 'PHYSICALID'.")
        df.rename(columns={cand: "PHYSICALID"}, inplace=True)

    df["PHYSICALID"] = (
        df["PHYSICALID"].astype(str).str.replace(",", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
        .astype("Int64")
    )
    if "the_geom" not in df.columns:
        raise ValueError("Centerline missing 'the_geom' WKT column.")

    geom = _parse_wkt_if_present(df["the_geom"])
    gdf = gpd.GeoDataFrame(df, geometry=geom, crs=CRS_WGS84).dropna(subset=["geometry"])
    return gdf.to_crs(CRS_METRIC)[["PHYSICALID", "the_geom", "geometry"]]


def load_classification(path: Path) -> pd.DataFrame:
    """
    Vehicle Classification Counts (wide by time-of-day or hour ranges).

    Accepts class column aliases:
      - 'Class Type', 'Veh Class Type', 'Vehicle Class', 'VehClassType'

    Accepts time headers like:
      - '12:00 AM'
      - '12:00-1:00 AM'
      - '12:00–1:00 AM' (unicode en-dash)
      - '12:00-1:00AM' (no space before AM/PM)
    """
    df = pd.read_csv(path, low_memory=False)
    # normalize header whitespace
    df = df.rename(columns=lambda c: str(c).strip())

    # SegmentID
    seg_col = next((c for c in df.columns if c.lower() == "segmentid"), None)
    if not seg_col:
        raise ValueError("Classification file missing 'SegmentID'.")
    df = df.rename(columns={seg_col: "SegmentID"})
    df["SegmentID"] = pd.to_numeric(df["SegmentID"], errors="coerce").astype("Int64")

    # Vehicle class column
    class_aliases = {"class type", "veh class type", "vehicle class", "vehclasstype"}
    cls_col = next((c for c in df.columns if c.strip().lower() in class_aliases), None)
    if not cls_col:
        raise ValueError("Classification file missing a vehicle class column (e.g., 'Class Type').")
    df = df.rename(columns={cls_col: "VehClassType"})
    df["VehClassType_norm"] = df["VehClassType"].astype(str).str.strip().str.lower()

    # Optional Date
    date_col = next((c for c in df.columns if c.strip().lower() == "date"), None)
    if date_col:
        df = df.rename(columns={date_col: "Date"})
    else:
        df["Date"] = pd.NaT

    # Time columns: single times OR ranges; allow -, – or — dash; optional space before AM/PM
    single_time_rx = re.compile(r"^\s*\d{1,2}:\d{2}\s*(AM|PM)\s*$", re.I)
    range_time_rx  = re.compile(r"^\s*\d{1,2}:\d{2}\s*[-–—]\s*\d{1,2}:\d{2}\s*(AM|PM)\s*$", re.I)
    range_time_rx2 = re.compile(r"^\s*\d{1,2}:\d{2}\s*[-–—]\s*\d{1,2}:\d{2}(AM|PM)\s*$", re.I)

    time_cols = [
        c for c in df.columns
        if (single_time_rx.match(c) or range_time_rx.match(c) or range_time_rx2.match(c))
    ]
    if not time_cols:
        raise ValueError("Could not find any time-of-day columns in classification file.")

    # Melt → long
    long = df[["SegmentID", "Date", "VehClassType_norm"] + time_cols].melt(
        id_vars=["SegmentID", "Date", "VehClassType_norm"],
        var_name="time",
        value_name="count",
    )
    long["count"] = pd.to_numeric(long["count"], errors="coerce").fillna(0)

    # Bucket vehicle classes
    CLASS_BUCKET_MAP = {
        # cars
        "auto": "cars", "taxis": "cars", "passenger": "cars",
        # trucks
        "commercial": "trucks", "medium truck": "trucks", "heavy truck": "trucks",
        "box truck": "trucks", "single unit truck": "trucks", "combination truck": "trucks",
        # buses
        "school bus": "buses", "other bus": "buses", "bus": "buses",
        # bikes
        "bicycle": "bikes", "bike": "bikes",
    }
    def bucket(v):
        return CLASS_BUCKET_MAP.get(str(v).strip().lower())

    long["bucket"] = long["VehClassType_norm"].map(bucket)
    long = long[long["bucket"].notna()].copy()

    # Aggregate per SegmentID (+Date) and bucket
    agg = (
        long.groupby(["SegmentID", "Date", "bucket"], dropna=False)["count"]
        .sum()
        .reset_index()
    )

    # Pivot to wide buckets
    pivot = agg.pivot_table(
        index=["SegmentID", "Date"],
        columns="bucket",
        values="count",
        aggfunc="sum",
        fill_value=0,
    ).reset_index()
    pivot.columns.name = None

    # Ensure all bucket columns exist
    for col in ["cars", "trucks", "buses", "bikes"]:
        if col not in pivot.columns:
            pivot[col] = 0.0

    pivot = pivot.rename(columns={
        "trucks": "class_trucks",
        "buses":  "class_buses",
        "bikes":  "class_bikes",
    })
    return pivot[["SegmentID", "Date", "cars", "class_trucks", "class_buses", "class_bikes"]]


def load_atr(path: Path) -> gpd.GeoDataFrame:
    df = pd.read_csv(path, low_memory=False)

    # Try WKT (NYSP feet) in 'WktGeom'
    wkt_col = next((c for c in df.columns if c.lower() == "wktgeom"), None)
    if wkt_col and df[wkt_col].astype(str).str.contains("POINT", na=False).any():
        geom = _parse_wkt_if_present(df[wkt_col])
        return gpd.GeoDataFrame(df, geometry=geom, crs=CRS_METRIC).dropna(subset=["geometry"])

    # Try WGS84 WKT in 'the_geom'
    the_geom = next((c for c in df.columns if c.lower() == "the_geom"), None)
    if the_geom and df[the_geom].astype(str).str.contains("POINT", na=False).any():
        geom = _parse_wkt_if_present(df[the_geom])
        gdf = gpd.GeoDataFrame(df, geometry=geom, crs=CRS_WGS84).dropna(subset=["geometry"])
        return gdf.to_crs(CRS_METRIC)

    # Try lon/lat
    lon_cand = next((c for c in df.columns if c.upper() in {"LON","LONG","LONGITUDE","POINT_X","X"}), None)
    lat_cand = next((c for c in df.columns if c.upper() in {"LAT","LATITUDE","POINT_Y","Y"}), None)
    if lon_cand and lat_cand:
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(pd.to_numeric(df[lon_cand], errors="coerce"),
                                        pd.to_numeric(df[lat_cand], errors="coerce")),
            crs=CRS_WGS84
        ).dropna(subset=["geometry"])
        return gdf.to_crs(CRS_METRIC)

    raise ValueError("ATR file missing parsable point geometry (no WktGeom/the_geom/ lon/lat).")

# ----------------- merge & aggregations -----------------

def merge_classification(center_gdf: gpd.GeoDataFrame, class_df: pd.DataFrame) -> gpd.GeoDataFrame:
    """Attach centerline geometry: SegmentID ↔ PHYSICALID."""
    left = class_df.copy()
    left["SegmentID"] = pd.to_numeric(left["SegmentID"], errors="coerce").astype("Int64")

    # PHYSICALID → geometry (unique)
    cid_lookup = (
        center_gdf[["PHYSICALID", "geometry"]]
        .drop_duplicates("PHYSICALID")
        .set_index("PHYSICALID")["geometry"]
    )

    line_geom = left["SegmentID"].map(cid_lookup)

    # Create GeoDataFrame, then set CRS explicitly (avoids GeoSeries crs bug)
    gdf = gpd.GeoDataFrame(left, geometry=line_geom)
    gdf = gdf.set_crs(CRS_METRIC, allow_override=True)
    gdf["PHYSICALID"] = gdf["SegmentID"]
    return gdf


def snap_atr_to_centerline(atr_gdf: gpd.GeoDataFrame, center_gdf: gpd.GeoDataFrame, max_ft: int) -> gpd.GeoDataFrame:
    joined = gpd.sjoin_nearest(
        atr_gdf,
        center_gdf[["PHYSICALID", "geometry"]],
        how="left",
        max_distance=max_ft,
        distance_col="dist_to_centerline_ft",
    ).drop(columns=["index_right"])
    return joined


def agg_classification_by_segment(class_joined: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Sum bucketed counts per PHYSICALID. Accepts columns:
      cars, class_trucks, class_buses, class_bikes (and optional Date).
    """
    df = class_joined.copy()

    grp = (
        df.groupby(["PHYSICALID"], dropna=True, as_index=False)[["cars", "class_trucks", "class_buses", "class_bikes"]]
        .sum()
    )
    grp["class_total"] = grp[["cars", "class_trucks", "class_buses", "class_bikes"]].sum(axis=1)

    # carry representative geometry
    geom_lookup = (
        class_joined.dropna(subset=["geometry"])
        .drop_duplicates("PHYSICALID")[["PHYSICALID", "geometry"]]
    )
    out = grp.merge(geom_lookup, on="PHYSICALID", how="left")
    return gpd.GeoDataFrame(out, geometry="geometry", crs=CRS_METRIC)


def agg_atr_by_segment(atr_joined: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Aggregate ATR volumes by PHYSICALID.
    We derive a row-total from any numeric volume-like columns available.
    """
    df = atr_joined.copy()
    # keep only matched to a centerline
    df = df[df["PHYSICALID"].notna()].copy()
    df["PHYSICALID"] = _coerce_int(df["PHYSICALID"])

    # detect total/volume-like columns
    vol_cols = [c for c in df.columns if re.search(r"(total|volume|veh)", c, re.I) and pd.api.types.is_numeric_dtype(df[c])]
    if not vol_cols:
        vol_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

    df["__atr_row_total__"] = df[vol_cols].sum(axis=1, min_count=1)

    agg = df.groupby("PHYSICALID", dropna=True, as_index=False).agg(
        atr_total_sum=("__atr_row_total__", "sum"),
        atr_total_mean=("__atr_row_total__", "mean"),
        atr_days=("__atr_row_total__", "count"),
    )
    return agg

# --------------------------- main ---------------------------

def main():
    ap = argparse.ArgumentParser(description="Merge & aggregate vehicle volumes/types with centerline geometry.")
    ap.add_argument("--classification", required=True, type=Path)
    ap.add_argument("--atr",           required=True, type=Path)
    ap.add_argument("--centerline",    required=True, type=Path)
    ap.add_argument("--out",           required=True, type=Path)
    ap.add_argument("--snap-ft",       type=int, default=120, help="Max snapping distance for ATR → centerline (feet)")
    args = ap.parse_args()

    # Load
    center = load_centerline(args.centerline)
    class_df = load_classification(args.classification)
    atr_gdf  = load_atr(args.atr)

    # 1) Classification: attach geometry, then aggregate per PHYSICALID
    class_joined = merge_classification(center, class_df)
    class_seg    = agg_classification_by_segment(class_joined)

    # 2) ATR → nearest centerline, then aggregate per PHYSICALID
    atr_joined = snap_atr_to_centerline(atr_gdf, center, max_ft=args.snap_ft)
    atr_seg    = agg_atr_by_segment(atr_joined)

    # 3) Combine per-segment metrics
    merged = class_seg.merge(atr_seg, on="PHYSICALID", how="outer")

    # 4) Export helpers: WKT + lon/lat from representative point
    gdf_wgs = merged.set_geometry("geometry").to_crs(CRS_WGS84)
    merged["geom_wkt"] = gdf_wgs.geometry.apply(lambda g: g.wkt if g is not None else None)
    rep = gdf_wgs.geometry.representative_point()
    merged["lon"] = rep.x
    merged["lat"] = rep.y

    # column order
    lead = [
        "PHYSICALID", "lon", "lat", "geom_wkt",
        "class_total", "cars", "class_trucks", "class_buses", "class_bikes",
        "atr_total_sum", "atr_total_mean", "atr_days",
    ]
    cols = [c for c in lead if c in merged.columns] + [c for c in merged.columns if c not in set(lead + ["geometry"])]
    out_df = merged.drop(columns=["geometry"]).reindex(columns=cols)

    # Save
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(args.out, index=False)
    print(f"✅ Saved {len(out_df):,} rows to {args.out}")
    print("   Columns:", list(out_df.columns))

if __name__ == "__main__":
    main()