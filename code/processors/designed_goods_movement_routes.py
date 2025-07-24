"""
NYC Truck Routes Post-Processor

This script reads the raw Truck Routes dataset and adds `latitude` and `longitude` columns
extracted from the `the_geom` WKT field. Keeps selected columns including `the_geom` and saves to a new CSV.
"""

import os
import pandas as pd
import re
import argparse


def extract_lat_lon(geom):
    """Extract (longitude, latitude) from WKT MULTILINESTRING or MULTIPOLYGON"""
    if isinstance(geom, str):
        match = re.search(r"\(\((-?\d+\.\d+) (-?\d+\.\d+)", geom)
        if match:
            return float(match.group(1)), float(match.group(2))
    return None, None


def main(input_path, output_path):
    df = pd.read_csv(input_path)

    df[['longitude', 'latitude']] = df['the_geom'].apply(
        lambda x: pd.Series(extract_lat_lon(x))
    )

    # Keep selected columns including the_geom
    KEEP_COLUMNS = [
        'Street',
        'RouteType',
        'TruckRoute',
        'BoroName',
        'the_geom',
        'longitude',
        'latitude'
    ]
    df = df[KEEP_COLUMNS]

    # Ensure the output folder exists
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    df.to_csv(output_path, index=False)
    print(f"Saved processed dataset with lat/lon to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Truck Routes CSV to extract lat/lon and clean columns.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input CSV file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output CSV file.")
    args = parser.parse_args()

    main(args.input, args.output)