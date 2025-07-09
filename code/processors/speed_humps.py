#!/usr/bin/env python3
"""
Speed Humps Post-Processor

This script reads the raw speed humps dataset and adds `latitude` and `longitude` columns
extracted from the `the_geom` WKT field. Saves the result to a new CSV file.

Usage:
    python processor_speed_humps.py -i ../downloaders/data/speed_humps.csv -o ../downloaders/data/speed_humps_with_latlon.csv
"""

import os
import pandas as pd
import re
import argparse

def extract_lat_lon(geom):
    """Extract (longitude, latitude) from WKT POINT or MULTIPOLYGON string"""
    if isinstance(geom, str):
        match = re.search(r"\(\((-?\d+\.\d+) (-?\d+\.\d+)", geom)
        if match:
            return float(match.group(1)), float(match.group(2))
    return None, None

def main(input_path, output_path):
    df = pd.read_csv(input_path)
    df[['longitude', 'latitude']] = df['the_geom'].apply(lambda x: pd.Series(extract_lat_lon(x)))

    # Ensure the output folder exists
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    # Save the processed file
    df.to_csv(output_path, index=False)
    print(f"✅ Saved processed dataset with lat/lon to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Speed Humps CSV to extract lat/lon.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input CSV file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output CSV file.")
    args = parser.parse_args()

    main(args.input, args.output)