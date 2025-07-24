#!/usr/bin/env python3
"""
Processor | Tree Cover & Landscaping ➜ Merge Turf Maintenance with Park Zones

Merges:
- Natural Turf Maintenance (point-based turf areas within parks)
- NYC Park Zones (polygonal park zones)

Join key: OMPPropID

Adds turf attributes to park zone geometries.
"""

from pathlib import Path
import argparse
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads

CRS_WGS84 = "EPSG:4326"
CRS_METRIC = "EPSG:2263"


# ── Loaders ────────────────────────────────────────────────────────────────

def load_parks_zones(path: Path) -> gpd.GeoDataFrame:
    df = pd.read_csv(path, low_memory=False)

    # Automatically detect geometry column
    geom_col = next((col for col in df.columns if 'polygon' in col.lower() or 'geom' in col.lower()), None)
    if not geom_col:
        raise ValueError("Could not find a valid geometry column (e.g., 'the_geom' or 'multipolygon') in parks_zones.")

    df["geometry"] = df[geom_col].apply(loads)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=CRS_WGS84)
    gdf = gdf.to_crs(CRS_METRIC)
    return gdf.drop(columns=[geom_col, "index_right"], errors="ignore")


def load_turf_sites(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    df = df[df["OMPPropID"].notna()].copy()
    return df


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--turf_maintenance", required=True, type=Path)
    ap.add_argument("--parks_zones", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    print("Loading turf maintenance …")
    turf_df = load_turf_sites(args.turf_maintenance)

    print("Loading parks zones …")
    parks_gdf = load_parks_zones(args.parks_zones)

    print("Merging by OMPPropID …")
    # Standardize join column name casing
    parks_gdf = parks_gdf.rename(columns={"OMPPROPID": "OMPPropID"})
    merged = parks_gdf.merge(turf_df, on="OMPPropID", how="left")

    print("Exporting results …")
    merged = merged.to_crs(CRS_WGS84)
    merged["lon"] = merged.geometry.centroid.x
    merged["lat"] = merged.geometry.centroid.y
    merged["geometry_wkt"] = merged.geometry.to_wkt()
    merged.drop(columns="geometry", inplace=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(args.output, index=False)
    print(f"merged file → {args.output}   rows={len(merged):,}")


if __name__ == "__main__":
    main()