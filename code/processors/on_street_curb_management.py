import argparse
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
import os

"""
This script merges NYC curb geometry data with nearby parking meters, loading zones, and truck routes
into a unified spatial dataset for on-street curb management analysis.

Key steps:
- Load curb data as multiline geometries.
- Convert all data to a common CRS for accurate spatial joins (EPSG:2263).
- Perform nearest spatial joins to associate curb segments with nearby functional elements.
- Export the enriched curb dataset as a CSV in WGS84 for interoperability.

"""

# === Notes on Spatial Resolution ===
# - All spatial joins and distance calculations are done using EPSG:2263 (NY State Plane), which uses feet/meters
#   and provides high-resolution accuracy suitable for street-level geometry.
# - Parking meters and loading zones are joined to curbs using a max search radius:
#     - Parking meters: 30 meters (to account for GPS inaccuracy and sidewalk offset)
#     - Loading zones and truck routes: 15 meters
# - The final exported dataset is reprojected to EPSG:4326 (WGS84) for use in web mapping tools.

# === Constants ===
WGS84 = "EPSG:4326"
NY_METRIC = "EPSG:2263"  # NY State Plane (in meters)

# === Helper for metric (EPSG:2263) point datasets ===
def to_gdf_metric(path, x_col, y_col):
    df = pd.read_csv(path)
    df = df.drop(columns=["index_right"], errors="ignore")
    df = df.dropna(subset=[x_col, y_col])
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[x_col], df[y_col]), crs=NY_METRIC)

# === Helper for lat/lon (EPSG:4326) point datasets ===
def to_gdf_wgs84(path, lon_col, lat_col):
    df = pd.read_csv(path)
    df = df.drop(columns=["index_right"], errors="ignore")
    df = df.dropna(subset=[lon_col, lat_col])
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=WGS84)
    return gdf.to_crs(NY_METRIC)

# === Helper: safe spatial join without clobbering index ===
def safe_sjoin_nearest(left, right, how="left", max_distance=15, distance_col=None):
    left = left.drop(columns=["index_right"], errors="ignore")
    right = right.drop(columns=["index_right"], errors="ignore")
    return gpd.sjoin_nearest(left, right, how=how, max_distance=max_distance, distance_col=distance_col)

def main():
    parser = argparse.ArgumentParser(description="Process and merge curb management datasets.")
    parser.add_argument("--curbs", required=True, help="Path to the curbs dataset (CSV)")
    parser.add_argument("--loading_zones", required=True, help="Path to the loading zones dataset (CSV)")
    parser.add_argument("--parking_meters", required=True, help="Path to the parking meters dataset (CSV)")
    parser.add_argument("--truck_routes", required=True, help="Path to the truck routes dataset (CSV)")
    parser.add_argument("--output", required=True, help="Path to save the processed output dataset (CSV)")
    args = parser.parse_args()

    # === Load base curb geometry ===
    curbs = pd.read_csv(args.curbs)
    curbs["geometry"] = curbs["the_geom"].apply(loads)
    curbs_gdf = gpd.GeoDataFrame(curbs, geometry="geometry", crs=WGS84)
    curbs_gdf = curbs_gdf.drop(columns=["the_geom", "index_right"], errors="ignore")
    curbs_proj = curbs_gdf.to_crs(NY_METRIC) # Convert to NY State Plane for accurate spatial joins

    # === Load functional layers ===
    loading = to_gdf_metric(args.loading_zones, "sign_x_coord", "sign_y_coord")
    meters = to_gdf_wgs84(args.parking_meters, "Longitude", "Latitude")

    trucks_raw = pd.read_csv(args.truck_routes)
    trucks_raw["geometry"] = trucks_raw["the_geom"].apply(loads)
    trucks_gdf = gpd.GeoDataFrame(trucks_raw, geometry="geometry", crs=WGS84)
    trucks = trucks_gdf.to_crs(NY_METRIC)

    # === Step 1: Join loading zones ===
    joined = safe_sjoin_nearest(curbs_proj, loading, distance_col="dist_to_loading")
    for col in loading.columns.drop("geometry", errors="ignore"):
        joined[f"loading_{col}"] = joined[col]
    joined = joined.drop(columns=loading.columns.drop("geometry", errors="ignore"), errors="ignore")

    # === Step 2: Join parking meters (increased distance tolerance to improve matches) ===
    joined = safe_sjoin_nearest(joined, meters, distance_col="dist_to_meter", max_distance=30)
    for col in meters.columns.drop("geometry", errors="ignore"):
        joined[f"meter_{col}"] = joined[col]
    joined = joined.drop(columns=meters.columns.drop("geometry", errors="ignore"), errors="ignore")

    # === Step 3: Join truck routes ===
    joined = safe_sjoin_nearest(joined, trucks, distance_col="dist_to_truck")
    for col in trucks.columns.drop("geometry", errors="ignore"):
        joined[f"truck_{col}"] = joined[col]
    joined = joined.drop(columns=trucks.columns.drop("geometry", errors="ignore"), errors="ignore")

    # === Final: Convert back to WGS84 and export ===
    final = joined.to_crs(WGS84)

    # Ensure the output folder exists
    output_folder = os.path.dirname(args.output)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    # Save the final dataset
    final.to_csv(args.output, index=False)
    print(f"SUCCESS: Final dataset saved ({len(final)} rows) at '{args.output}'")

if __name__ == "__main__":
    main()