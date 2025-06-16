#!/usr/bin/env python3
"""
Processor: Combine NYC pedestrian ramp locations and accessible pedestrian signal locations
into a single unified geospatial dataset for transit stop accessibility.
"""

import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
import os

# === Constants ===
DATA_DIR = "data/transit_stop_accessibility"
OUTPUT_PATH = os.path.join(DATA_DIR, "transit_stop_accessibility.csv")
WGS84 = "EPSG:4326"

# === Helper: Convert WKT geometry column to GeoDataFrame
def to_gdf_from_geom(df, geom_col, source_name):
    df = df.copy()
    df["geometry"] = df[geom_col].apply(loads)
    df["source"] = source_name
    return gpd.GeoDataFrame(df, geometry="geometry", crs=WGS84)

# === Load datasets
ped_ramps = pd.read_csv(os.path.join(DATA_DIR, "pedestrian_ramp_locations.csv"))
aps_signals = pd.read_csv(os.path.join(DATA_DIR, "accessible_pedestrian_signal_locations.csv"))

# === Convert to GeoDataFrames using 'the_geom'
gdf_ramps = to_gdf_from_geom(ped_ramps, geom_col="the_geom", source_name="pedestrian_ramp")
gdf_signals = to_gdf_from_geom(aps_signals, geom_col="the_geom", source_name="accessible_signal")

# === Merge and save
# === Merge and save
merged = pd.concat([gdf_ramps, gdf_signals], ignore_index=True)
merged.to_csv(OUTPUT_PATH, index=False)

print(f"Transit Stop Accessibility dataset saved to: {OUTPUT_PATH}")
print(f"Total records: {len(merged)}")
