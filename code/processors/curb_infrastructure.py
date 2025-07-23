#!/usr/bin/env python3
"""
Processor | Curb Infrastructure ➜ Sidewalk merge

Merges sidewalk geometries with nearby:
- pedestrian ramps
- raised crosswalks
- medians

Output includes geometry, centroids (lon/lat), and WKT.
"""

from pathlib import Path
import argparse
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads

CRS_WGS84 = "EPSG:4326"
CRS_METRIC = "EPSG:2263"  # NY State Plane (ft/m)

# ── Loaders ────────────────────────────────────────────────────────────────

def load_sidewalks(p: Path) -> gpd.GeoDataFrame:
    df = pd.read_csv(p, low_memory=False)
    df["geometry"] = df["the_geom"].apply(loads)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=CRS_WGS84)
    return gdf.drop(columns=["the_geom", "index_right"], errors="ignore").to_crs(CRS_METRIC)

def load_wkt_pts(p: Path, keep: list[str]) -> gpd.GeoDataFrame:
    df = pd.read_csv(p, low_memory=False)
    df = df[df["the_geom"].notna()].copy()
    df["geometry"] = df["the_geom"].apply(loads)
    df = df[[c for c in keep if c in df.columns] + ["geometry"]]
    return gpd.GeoDataFrame(df, geometry="geometry", crs=CRS_WGS84).to_crs(CRS_METRIC)

def load_xy_pts(p: Path, xcol: str, ycol: str, keep: list[str]) -> gpd.GeoDataFrame:
    df = pd.read_csv(p, low_memory=False)
    df = df[[c for c in keep if c in df.columns] + [xcol, ycol]].copy()
    df.dropna(subset=[xcol, ycol], inplace=True)
    df[xcol] = pd.to_numeric(df[xcol], errors="coerce")
    df[ycol] = pd.to_numeric(df[ycol], errors="coerce")
    df.dropna(subset=[xcol, ycol], inplace=True)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[xcol], df[ycol]), crs=CRS_METRIC)
    return gdf

# ── Join helper ────────────────────────────────────────────────────────────

def attach(base: gpd.GeoDataFrame, pts: gpd.GeoDataFrame, dmax: float, dist_col: str, prefix: str):
    joined = gpd.sjoin_nearest(base, pts, how="left", max_distance=dmax, distance_col=dist_col)

    attrs = (
        pts.drop(columns="geometry")
            .add_prefix(prefix + "_")
            .reset_index()
            .rename(columns={"index": "index_right"})
    )

    joined = joined.merge(attrs, on="index_right", how="left")
    return joined.drop(columns="index_right")

# ── Main ───────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sidewalks", required=True, type=Path)
    ap.add_argument("--pedestrian_ramps", required=True, type=Path)
    ap.add_argument("--raised_crosswalks", required=True, type=Path)
    ap.add_argument("--medians", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    print("Loading base sidewalk geometries …")
    base = load_sidewalks(args.sidewalks)

    print("Joining pedestrian ramps …")
    ramps_keep = ["source_id", "status", "type"]
    ramps = load_wkt_pts(args.pedestrian_ramps, ramps_keep)
    base = attach(base, ramps, 15, "dist_ramp", "ramp")

    print("Joining raised crosswalks …")
    raised_keep = ["id", "status"]
    raised = load_xy_pts(args.raised_crosswalks, "X", "Y", raised_keep)
    base = attach(base, raised, 15, "dist_raised", "raised")

    print("Joining medians …")
    med_keep = ["source_id", "status"]
    medians = load_wkt_pts(args.medians, med_keep)
    base = attach(base, medians, 15, "dist_median", "median")

    print("Exporting results …")
    base = base.to_crs(CRS_WGS84)
    base["lon"] = base.geometry.centroid.x
    base["lat"] = base.geometry.centroid.y
    base["geometry_wkt"] = base.geometry.to_wkt()
    base.drop(columns="geometry", inplace=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    base.to_csv(args.output, index=False)
    print(f"merged file → {args.output}   rows={len(base):,}")

if __name__ == "__main__":
    main()