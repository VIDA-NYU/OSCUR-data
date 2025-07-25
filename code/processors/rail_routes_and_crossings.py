import argparse
import os
import pandas as pd
import geopandas as gpd
from shapely import wkt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--crossings", required=True, help="CSV of rail crossings (points)")
    parser.add_argument("--railroads", required=True, help="CSV of railroad lines (MultiLineString)")
    parser.add_argument("--output", required=True, help="Path to save merged CSV")
    args = parser.parse_args()

    # --- Load crossings (assumed to be POINTS) ---
    crossings_df = pd.read_csv(args.crossings)
    crossings_df["geometry"] = crossings_df["the_geom"].apply(wkt.loads)
    crossings_gdf = gpd.GeoDataFrame(crossings_df, geometry="geometry", crs="EPSG:4326").to_crs(epsg=2263)

    # --- Load railroads (assumed to be LINESTRING or MULTILINESTRING) ---
    railroads_df = pd.read_csv(args.railroads)
    railroads_df["geometry"] = railroads_df["the_geom"].apply(wkt.loads)
    railroads_gdf = gpd.GeoDataFrame(railroads_df, geometry="geometry", crs="EPSG:4326").to_crs(epsg=2263)

    # --- Save original geometries as WKT for export (optional) ---
    railroads_gdf["rail_geom"] = railroads_gdf.geometry
    crossings_gdf["crossing_geom"] = crossings_gdf.geometry

    # --- Spatial join: left join from railroads to crossings ---
    merged = gpd.sjoin_nearest(
        railroads_gdf,
        crossings_gdf[["crossing_geom", "geometry"]],
        how="left",
        distance_col="distance_to_crossing"
    )

    # --- Convert WKT columns for export ---
    merged["rail_geom"] = merged["rail_geom"].apply(lambda g: g.wkt if g else None)
    merged["crossing_geom"] = merged["crossing_geom"].apply(lambda g: g.wkt if g else None)

    # --- Drop geometry and any internal columns ---
    merged = merged.drop(columns=["geometry", "index_right"], errors="ignore")

    # --- Ensure output directory exists ---
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # --- Export ---
    merged.to_csv(args.output, index=False)
    print(f"Saved merged file to {args.output}")

if __name__ == "__main__":
    main()