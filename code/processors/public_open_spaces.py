#!/usr/bin/env python3
"""
Processor | Multi-use Paths ➜ Merge

Combines:
- Open Space (Other)
- NYC Open Streets
Joined to:
- NYC Street Centerlines (CSCL)

Output includes geometry, centroids (lon/lat), and WKT.
"""

from pathlib import Path
import argparse
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
from shapely.geometry import Point

CRS_WGS84 = "EPSG:4326"
CRS_METRIC = "EPSG:2263"

def load_polygons(path: Path, geom_col: str, keep: list[str]) -> gpd.GeoDataFrame:
    df = pd.read_csv(path, low_memory=False)
    df = df[df[geom_col].notna()].copy()
    df["geometry"] = df[geom_col].apply(loads)
    if keep:
        df = df[[*keep, "geometry"]]
    return gpd.GeoDataFrame(df, geometry="geometry", crs=CRS_WGS84).to_crs(CRS_METRIC)


def load_lines(path: Path, geom_col: str, keep: list[str]) -> gpd.GeoDataFrame:
    df = pd.read_csv(path, low_memory=False)

    # Sanitize column names
    df.columns = df.columns.str.strip()

    if geom_col not in df.columns:
        raise KeyError(f"Geometry column '{geom_col}' not found in CSV. Columns present: {df.columns.tolist()}")

    df = df[df[geom_col].notna()].copy()
    df["geometry"] = df[geom_col].apply(loads)
    df = df[[*keep, "geometry"]]
    return gpd.GeoDataFrame(df, geometry="geometry", crs=CRS_WGS84).to_crs(CRS_METRIC)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--open_spaces", required=True, type=Path)
    ap.add_argument("--open_streets", required=True, type=Path)
    ap.add_argument("--centerlines", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    print("Loading base centerlines …")
    centerlines = load_lines(args.centerlines, geom_col="the_geom", keep=["PHYSICALID"])

    print("Joining Open Space (Other) polygons …")
    open_spaces = load_polygons(args.open_spaces, geom_col="the_geom", keep=["NAME", "STATUS"])
    open_spaces = gpd.sjoin_nearest(open_spaces, centerlines, how="left", max_distance=20)
    open_spaces["source"] = "open_space_other"

    print("Joining Open Streets lines …")
    open_streets = load_lines(args.open_streets, geom_col="The_Geom", keep=["segmentidt", "Borough Name"])
    open_streets = gpd.sjoin_nearest(open_streets, centerlines, how="left", max_distance=20)
    open_streets["source"] = "open_streets"

    print("Merging …")
    merged = pd.concat([open_spaces, open_streets], ignore_index=True)
    merged = merged.to_crs(CRS_WGS84)
    merged["lon"] = merged.geometry.centroid.x
    merged["lat"] = merged.geometry.centroid.y
    merged["geometry_wkt"] = merged.geometry.to_wkt()
    merged = merged.drop(columns=["geometry"])

    print("Saving to CSV …")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(args.output, index=False)
    print(f"Merged dataset → {args.output}   rows={len(merged):,}")

if __name__ == "__main__":
    main()