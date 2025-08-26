#!/usr/bin/env python3
"""
Processor | Speed Distributions ➜ Add midpoint lat/lon
- Input:  CSV with a 'link_points' column (DOT Traffic Speeds NBE or similar)
- Output: Same CSV columns + two new columns: lat, lon (midpoint per record)
- No hardcoded paths; fully CLI-driven; chunked to handle large files.

Run (example):
python -m code.processors.speed_distributions/add_midpoints.py \
  --input data/speed_distributions/traffic_speeds_sample.csv \
  --output data/speed_distributions/traffic_speeds_with_midpoints.csv
"""

from __future__ import annotations
from pathlib import Path
import argparse
import math
import re
import pandas as pd

LAT_MIN, LAT_MAX = 39.0, 42.0
LON_MIN, LON_MAX = -76.0, -71.0
NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")

def parse_midpoint(link_points: str) -> tuple[float, float] | tuple[None, None]:
    if not isinstance(link_points, str) or not link_points.strip():
        return (None, None)

    nums = [float(x) for x in NUM_RE.findall(link_points)]
    if len(nums) < 2:
        return (None, None)

    pairs = list(zip(nums[0::2], nums[1::2]))
    if not pairs:
        return (None, None)

    a0, b0 = pairs[0]

    def looks_latlon(a, b):  # (lat, lon)
        return LAT_MIN <= a <= LAT_MAX and LON_MIN <= b <= LON_MAX

    def looks_lonlat(a, b):  # (lon, lat)
        return LON_MIN <= a <= LON_MAX and LAT_MIN <= b <= LAT_MAX

    swap = False
    if looks_latlon(a0, b0):
        swap = False
    elif looks_lonlat(a0, b0):
        swap = True
    else:
        swap = looks_latlon(b0, a0)

    if swap:
        first_lat, first_lon = pairs[0][1], pairs[0][0]
        last_lat, last_lon  = pairs[-1][1], pairs[-1][0]
    else:
        first_lat, first_lon = pairs[0][0], pairs[0][1]
        last_lat, last_lon  = pairs[-1][0], pairs[-1][1]

    lat = (first_lat + last_lat) / 2.0
    lon = (first_lon + last_lon) / 2.0

    if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
        return (None, None)
    if any(math.isnan(v) for v in (lat, lon)):
        return (None, None)

    return (lat, lon)

def process(input_csv: Path, output_csv: Path, link_col: str, chunksize: int) -> int:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    header_written = False
    total = 0

    for chunk in pd.read_csv(input_csv, low_memory=False, chunksize=chunksize):
        if link_col not in chunk.columns:
            raise ValueError(f"Missing required column '{link_col}'. "
                             f"Found columns: {list(chunk.columns)[:15]}...")

        coords = chunk[link_col].apply(parse_midpoint)
        chunk["lat"] = [c[0] for c in coords]
        chunk["lon"] = [c[1] for c in coords]

        mode = "a" if header_written else "w"
        chunk.to_csv(output_csv, index=False, mode=mode, header=not header_written)
        header_written = True
        total += len(chunk)

    return total

def main():
    ap = argparse.ArgumentParser(description="Append midpoint lat/lon columns to traffic speed dataset.")
    ap.add_argument("--input", required=True, type=Path, help="Input CSV path")
    ap.add_argument("--output", required=True, type=Path, help="Output CSV path")
    ap.add_argument("--link-col", default="link_points", help="Name of the link_points column")
    ap.add_argument("--chunksize", type=int, default=250_000, help="Rows per chunk to process")
    args = ap.parse_args()

    total = process(args.input, args.output, args.link_col, args.chunksize)
    print(f"✅ Processed {total:,} rows → {args.output}")

if __name__ == "__main__":
    main()
