#!/usr/bin/env python3
"""
Bicycle & Pedestrian Trip Counts | Attach Locations to Bicycle Counts
─────────────────────────────────────────────────────────────────────
Left-join Bicycle Counts with Bicycle Counters on `id` and bring in
point location (lon/lat + WKT). No hardcoded paths.

Run (example):
python -m code.processors.bicycle_pedestrian_trip_counts.merge_bicycle_counts_with_locations \
  --counts  data/bicycle_pedestrian_trip_counts/bicycle_counts.csv \
  --counters data/bicycle_pedestrian_trip_counts/bicycle_counters.csv \
  --out    data/bicycle_pedestrian_trip_counts/bicycle_counts_with_locations.csv
"""

from pathlib import Path
import argparse
import re
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
from shapely.geometry import Point

CRS_WGS84  = "EPSG:4326"

# ---------- helpers ----------

def _lower_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    ren = {c: c.strip() for c in df.columns}  # trim whitespace
    df = df.rename(columns=ren)
    # stable case-insensitive access by keeping originals but providing a lookup helper
    return df

def _find_col(cols, *candidates):
    """Return first column from candidates found in cols (case-insensitive)."""
    lower = {c.lower(): c for c in cols}
    for cand in candidates:
        if cand in cols:
            return cand
        if cand.lower() in lower:
            return lower[cand.lower()]
    return None

def _geometry_from_any(df: pd.DataFrame) -> gpd.GeoSeries:
    """
    Build a GeoSeries (WGS84) from common geometry encodings present in NYC Open Data exports.
    Supports WKT (WktGeom/the_geom/WKT/geometry) or XY numeric columns.
    """
    cols = list(df.columns)

    # 1) WKT columns
    wkt_col = _find_col(cols, "WktGeom", "the_geom", "WKT", "geometry", "GEOMETRY")
    if wkt_col is not None and df[wkt_col].astype(str).str.contains(r"[A-Z]+\s*\(", na=False).any():
        gs = df[wkt_col].apply(lambda s: loads(str(s)) if isinstance(s, str) else None)
        return gpd.GeoSeries(gs, crs=CRS_WGS84)

    # 2) Lat/Lon numeric pairs (common names)
    lon_col = _find_col(cols, "Longitude", "LONGITUDE", "POINT_X", "X", "lon")
    lat_col = _find_col(cols, "Latitude", "LATITUDE", "POINT_Y", "Y", "lat")
    if lon_col and lat_col:
        lon = pd.to_numeric(df[lon_col], errors="coerce")
        lat = pd.to_numeric(df[lat_col], errors="coerce")
        pts = gpd.points_from_xy(lon, lat, crs=CRS_WGS84)
        return gpd.GeoSeries(pts, crs=CRS_WGS84)

    # 3) Socrata "location" field sometimes split; if present, try LOCATION.longitude/latitude
    lon_alt = _find_col(cols, "location.longitude")
    lat_alt = _find_col(cols, "location.latitude")
    if lon_alt and lat_alt:
        lon = pd.to_numeric(df[lon_alt], errors="coerce")
        lat = pd.to_numeric(df[lat_alt], errors="coerce")
        pts = gpd.points_from_xy(lon, lat, crs=CRS_WGS84)
        return gpd.GeoSeries(pts, crs=CRS_WGS84)

    raise ValueError("No parsable geometry found (tried WKT columns and common lon/lat column names).")

# ---------- loaders ----------

def load_counts(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    df = _lower_names(df)
    # normalize join key
    id_col = _find_col(df.columns, "id")
    if id_col is None:
        raise ValueError("Bicycle Counts file must contain an 'id' column.")
    df.rename(columns={id_col: "id"}, inplace=True)
    df["id"] = df["id"].astype(str)
    return df

def load_counters(path: Path) -> gpd.GeoDataFrame:
    df = pd.read_csv(path, low_memory=False)
    df = _lower_names(df)
    id_col = _find_col(df.columns, "id")
    if id_col is None:
        raise ValueError("Bicycle Counters file must contain an 'id' column.")
    df.rename(columns={id_col: "id"}, inplace=True)
    df["id"] = df["id"].astype(str)

    geom = _geometry_from_any(df)
    gdf = gpd.GeoDataFrame(df, geometry=geom).dropna(subset=["geometry"]).set_crs(CRS_WGS84)
    return gdf

# ---------- processing ----------

def merge_counts_with_locations(counts: pd.DataFrame, counters: gpd.GeoDataFrame) -> pd.DataFrame:
    # Keep a few likely useful metadata fields from counters if they exist
    maybe_meta = ["name", "site_name", "counter_name", "location", "borough", "boro", "direction"]
    keep_meta = [c for c in counters.columns if c in maybe_meta]

    counters_min = counters[["id", "geometry"] + keep_meta].copy()

    merged = counts.merge(counters_min, on="id", how="left", validate="m:1")

    # Coordinates + WKT
    lon = merged["geometry"].apply(lambda g: g.x if g is not None else None)
    lat = merged["geometry"].apply(lambda g: g.y if g is not None else None)
    wkt = merged["geometry"].apply(lambda g: g.wkt if g is not None else None)

    merged["lon"] = lon
    merged["lat"] = lat
    merged["geom_wkt"] = wkt

    # Drop the shapely geometry column for a flat CSV
    merged = merged.drop(columns=["geometry"])

    return merged

# ---------- CLI ----------

def main() -> None:
    ap = argparse.ArgumentParser(description="Merge Bicycle Counts with Bicycle Counters (locations) on `id`.")
    ap.add_argument("--counts",  required=True, type=Path, help="CSV of Bicycle Counts (must have 'id').")
    ap.add_argument("--counters", required=True, type=Path, help="CSV of Bicycle Counters (must have 'id' and location).")
    ap.add_argument("--out",     required=True, type=Path, help="Output CSV path.")
    args = ap.parse_args()

    counts_df   = load_counts(args.counts)
    counters_gd = load_counters(args.counters)

    merged = merge_counts_with_locations(counts_df, counters_gd)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(args.out, index=False)
    matched = merged["geom_wkt"].notna().sum()
    print(f"✅ Saved {len(merged):,} rows → {args.out} | matched locations: {matched:,} ({matched/len(merged)*100:.1f}%)")

if __name__ == "__main__":
    main()
