import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
import argparse
import os

"""
Processor: Merge NYC Sidewalks with Telecom Poles and Street Sign Work Orders.

Usage:
python code/processors/fixed_obstructions.py \
  --sidewalks data/fixed_obstructions/sidewalk_planimetric.csv \
  --telecom_poles data/fixed_obstructions/telecom_franchise_poles.csv \
  --street_signs data/fixed_obstructions/street_sign_work_orders.csv \
  --output data/fixed_obstructions/sidewalks_with_obstructions.csv
"""

WGS84 = "EPSG:4326"
NY_METRIC = "EPSG:2263"


def load_sidewalks(path):
    df = pd.read_csv(path)
    df["geometry"] = df["the_geom"].apply(loads)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=WGS84)
    return gdf.drop(columns=["the_geom", "index_right"], errors="ignore").to_crs(NY_METRIC)


def load_points(path, x_col, y_col, dedup_cols):
    df = pd.read_csv(path)
    df = df.drop(columns=["index_right"], errors="ignore").dropna(subset=[x_col, y_col])
    df = df.drop_duplicates(subset=dedup_cols)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[x_col], df[y_col]), crs=NY_METRIC)
    return gdf


def safe_sjoin_nearest(left, right, prefix, max_distance=10):
    left = left.drop(columns=["index_right"], errors="ignore").copy()
    right = right.drop(columns=["index_right"], errors="ignore").copy()
    joined = gpd.sjoin_nearest(left, right, how="left", max_distance=max_distance, distance_col=f"{prefix}_dist")
    for col in right.columns.drop("geometry", errors="ignore"):
        joined[f"{prefix}_{col}"] = joined[col]
    return joined.drop(columns=right.columns.drop("geometry", errors="ignore").tolist() + ["index_right"], errors="ignore")


def main(args):
    sidewalks = load_sidewalks(args.sidewalks)
    telecom = load_points(args.telecom_poles, "X Coord.", "Y Coord.", ["X Coord.", "Y Coord."])
    signs = load_points(args.street_signs, "sign_x_coord", "sign_y_coord", ["sign_x_coord", "sign_y_coord"])

    joined = safe_sjoin_nearest(sidewalks, telecom, prefix="telecom")
    joined = safe_sjoin_nearest(joined, signs, prefix="sign")

    final = joined.to_crs(WGS84)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    final.to_csv(args.output, index=False)
    print(f"SUCCESS: Final dataset saved with {len(final)} rows at '{args.output}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge sidewalks with telecom poles and street signs.")
    parser.add_argument("--sidewalks", required=True, help="Path to sidewalk CSV")
    parser.add_argument("--telecom_poles", required=True, help="Path to telecom poles CSV")
    parser.add_argument("--street_signs", required=True, help="Path to street signs CSV")
    parser.add_argument("--output", required=True, help="Path to save output CSV")

    args = parser.parse_args()
    main(args)