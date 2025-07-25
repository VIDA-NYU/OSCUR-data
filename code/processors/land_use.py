#!/usr/bin/env python3
"""
Processor | Land Use ➜ Sidewalk merge

Spatially joins sidewalk polygons with nearby:
- facilities (public buildings: schools, libraries, etc.)
- licensed businesses (from citywide license database)

Each sidewalk polygon is enriched with proximity data to surrounding land uses.
"""

from pathlib import Path
import argparse
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads

CRS_WGS84 = "EPSG:4326"
CRS_METRIC = "EPSG:2263"  # NY State Plane

# ── Loaders ────────────────────────────────────────────────────────────────

def load_sidewalks(p: Path) -> gpd.GeoDataFrame:
    df = pd.read_csv(p, low_memory=False)
    df["geometry"] = df["the_geom"].apply(loads)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=CRS_WGS84)
    return gdf.drop(columns=["the_geom", "index_right"], errors="ignore").to_crs(CRS_METRIC)

def load_facilities(p: Path, keep: list[str]) -> gpd.GeoDataFrame:
    df = pd.read_csv(p, low_memory=False)
    df = df[df["latitude"].notna() & df["longitude"].notna()].copy()
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df.dropna(subset=["latitude", "longitude"], inplace=True)
    df = df[[c for c in keep if c in df.columns] + ["latitude", "longitude"]].copy()
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"]), crs=CRS_WGS84)
    return gdf.to_crs(CRS_METRIC)

def load_licenses(p: Path, keep: list[str]) -> gpd.GeoDataFrame:
    df = pd.read_csv(p, low_memory=False)
    df = df[[c for c in keep if c in df.columns] + ["Longitude", "Latitude"]].copy()
    df.dropna(subset=["Longitude", "Latitude"], inplace=True)
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df.dropna(subset=["Longitude", "Latitude"], inplace=True)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["Longitude"], df["Latitude"]), crs=CRS_WGS84)
    return gdf.to_crs(CRS_METRIC)

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
    ap.add_argument("--facilities", required=True, type=Path)
    ap.add_argument("--licenses", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    print("Loading base sidewalk geometries …")
    base = load_sidewalks(args.sidewalks)

    print("Joining public facilities …")
    fac_keep = ["facility_name", "facility_type", "agency", "boro"]
    facilities = load_facilities(args.facilities, fac_keep)
    base = attach(base, facilities, 20, "dist_facility", "fac")

    print("Joining licensed businesses …")
    lic_keep = ["license_type", "business_name", "license_status", "industry"]
    licenses = load_licenses(args.licenses, lic_keep)
    base = attach(base, licenses, 20, "dist_license", "biz")

    print("Exporting results …")
    base = base.to_crs(CRS_WGS84)
    base["lon"] = base.geometry.centroid.x
    base["lat"] = base.geometry.centroid.y
    base["geometry_wkt"] = base.geometry.to_wkt()
    base.drop(columns="geometry", inplace=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    base.to_csv(args.output, index=False)
    print(f"✔ merged file → {args.output}   rows={len(base):,}")

if __name__ == "__main__":
    main()