#!/usr/bin/env python3
"""
Processor | Roadway Features → Merge on Centerlines
Joins centerlines with intersections (points), corridors (lines), bus lanes (lines),
and block faces (points with mid_long/mid_lat) using nearest spatial join.

- Robust geometry loader:
  * WKT in 'the_geom' or 'geometry'
  * Lon/lat pairs in any of:
      ('Longitude','Latitude'), ('longitude','latitude'),
      ('lon','lat'), ('POINT_X','POINT_Y'), ('x','y'),
      ('mid_long','mid_lat')
- CRS: operations in EPSG:2263, output in EPSG:4326
- Keeps all columns from joined layers (with prefixes)
"""

from pathlib import Path
import argparse
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads

CRS_WGS84  = "EPSG:4326"
CRS_METRIC = "EPSG:2263"  # NY State Plane


# ───────────────────────── helpers ─────────────────────────

def _first_lonlat_pair(df: pd.DataFrame):
    """Return the first (lon_col, lat_col) pair present in df, else (None, None)."""
    candidates = [
        ("Longitude", "Latitude"),
        ("longitude", "latitude"),
        ("lon", "lat"),
        ("POINT_X", "POINT_Y"),
        ("x", "y"),
        ("mid_long", "mid_lat"),
    ]
    for lo, la in candidates:
        if lo in df.columns and la in df.columns:
            return lo, la
    return None, None


def load_any_geometry(path: Path) -> gpd.GeoDataFrame:
    """
    Load a CSV as GeoDataFrame from either:
      - WKT in 'the_geom' or 'geometry'
      - Any recognized lon/lat pair (incl. 'mid_long'/'mid_lat')
    Assumes CRS_WGS84 on input; caller can reproject.
    """
    df = pd.read_csv(path, low_memory=False)

    # 1) WKT route
    for wkt_col in ("the_geom", "geometry"):
        if wkt_col in df.columns:
            # tolerate empty/invalid rows
            gseries = df[wkt_col].dropna().astype(str)
            # Some NYC Open Data puts empty strings; coerce safely
            geom = gseries.apply(lambda s: loads(s) if s and s.strip() else None)
            # Build aligned geometry column
            geom_full = pd.Series(index=df.index, dtype=object)
            geom_full.loc[geom.index] = geom.values
            gdf = gpd.GeoDataFrame(df, geometry=geom_full, crs=CRS_WGS84)
            return gdf

    # 2) Lon/Lat route
    lon_col, lat_col = _first_lonlat_pair(df)
    if lon_col and lat_col:
        # coerce numerics and drop invalids
        df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")
        df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
        df = df.dropna(subset=[lon_col, lat_col]).copy()
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
            crs=CRS_WGS84,
        )
        return gdf

    raise ValueError(
        f"Could not find geometry in {path} (no WKT and no recognized lon/lat columns)."
    )


def sjoin_nearest_keep_all(base: gpd.GeoDataFrame,
                           other: gpd.GeoDataFrame,
                           prefix: str,
                           max_distance: float,
                           distance_col: str) -> gpd.GeoDataFrame:
    """
    sjoin_nearest but keeps ALL columns from `other`, prefixed.
    Avoids index_right pollution and preserves base geometry.
    """
    # run join
    joined = gpd.sjoin_nearest(
        base.drop(columns=["index_right"], errors="ignore"),
        other.drop(columns=["index_right"], errors="ignore"),
        how="left",
        max_distance=max_distance,
        distance_col=distance_col,
    )

    # collect the matched rows from `other` for attribute copy
    if "index_right" in joined.columns:
        right_idx = joined["index_right"]
        attrs = other.drop(columns=["geometry"], errors="ignore").reset_index()
        attrs = attrs.rename(columns={"index": "index_right"})
        joined = joined.merge(attrs, on="index_right", how="left")
        joined = joined.drop(columns=["index_right"])

    # prefix everything that came from `other`
    # detect newly-added cols (exclude original base cols)
    base_cols = set(base.columns)
    base_cols.add("geometry")
    new_cols = [c for c in joined.columns if c not in base_cols]
    rename_map = {c: f"{prefix}_{c}" for c in new_cols}
    joined = joined.rename(columns=rename_map)

    return joined


# ───────────────────────── main ─────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Merge roadway feature layers onto centerlines (nearest-join)."
    )
    ap.add_argument("--centerlines", required=True, type=Path)
    ap.add_argument("--intersections", required=True, type=Path)
    ap.add_argument("--corridors", required=True, type=Path)
    ap.add_argument("--bus_lanes", required=True, type=Path)
    ap.add_argument("--block_face", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    print("• Loading Centerlines …")
    center = load_any_geometry(args.centerlines).to_crs(CRS_METRIC)

    print("• Loading Intersections (points) …")
    inter = load_any_geometry(args.intersections).to_crs(CRS_METRIC)

    print("• Loading Corridors (lines) …")
    cor = load_any_geometry(args.corridors).to_crs(CRS_METRIC)

    print("• Loading Bus Lanes (lines) …")
    bus = load_any_geometry(args.bus_lanes).to_crs(CRS_METRIC)

    print("• Loading Block Face (points via mid_long/mid_lat if present) …")
    block = load_any_geometry(args.block_face).to_crs(CRS_METRIC)

    # Nearest joins — tweak radii if needed
    print("• Joining Intersections → Centerlines …")
    merged = sjoin_nearest_keep_all(center, inter, prefix="int", max_distance=25, distance_col="int_dist_m")

    print("• Joining Corridors → Centerlines …")
    merged = sjoin_nearest_keep_all(merged, cor, prefix="cor", max_distance=25, distance_col="cor_dist_m")

    print("• Joining Bus Lanes → Centerlines …")
    merged = sjoin_nearest_keep_all(merged, bus, prefix="bus", max_distance=25, distance_col="bus_dist_m")

    print("• Joining Block Face → Centerlines …")
    merged = sjoin_nearest_keep_all(merged, block, prefix="blk", max_distance=25, distance_col="blk_dist_m")

    # Finalize for CSV output
    print("• Finalizing export …")
    merged_wgs = merged.to_crs(CRS_WGS84).copy()
    merged_wgs["centerline_wkt"] = merged_wgs.geometry.to_wkt()
    merged_wgs["lon"] = merged_wgs.geometry.centroid.x
    merged_wgs["lat"] = merged_wgs.geometry.centroid.y
    merged_wgs = merged_wgs.drop(columns=["geometry"])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    merged_wgs.to_csv(args.out, index=False)
    print(f"✔ Saved {len(merged_wgs):,} rows → {args.out}")


if __name__ == "__main__":
    main()