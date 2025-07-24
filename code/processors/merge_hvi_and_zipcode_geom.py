#!/usr/bin/env python3
"""
Merge Heat Vulnerability Index data with Modified ZIP Code Tabulation Areas (MODZCTA) geometry
───────────────────────────────────────────────────────────────────────────────────────────────
Joins HVI scores (by `zcta20`) with ZIP Code polygons (by `MODZCTA`) using a left join.
"""

from pathlib import Path
import argparse, pandas as pd

def main() -> None:
    ap = argparse.ArgumentParser(description="Merge HVI with MODZCTA polygons")
    ap.add_argument("--hvi", required=True, type=Path, help="CSV of Heat Vulnerability Index")
    ap.add_argument("--zipcode_geom", required=True, type=Path, help="CSV of MODZCTA polygons with geometry")
    ap.add_argument("--out", required=True, type=Path, help="Output CSV path")
    args = ap.parse_args()

    # Load datasets
    hvi = pd.read_csv(args.hvi, dtype=str, low_memory=False)
    zip_geom = pd.read_csv(args.zipcode_geom, dtype=str, low_memory=False)

    # Merge on ZIP code (zcta20 from HVI, MODZCTA from geometry)
    hvi.columns = hvi.columns.str.strip()
    zip_geom.columns = zip_geom.columns.str.strip()

    merged = zip_geom.merge(hvi, left_on="MODZCTA", right_on="ZIP Code Tabulation Area (ZCTA) 2020", how="left")

    # Save
    args.out.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(args.out, index=False)

    print(f"Merged dataset saved: {args.out} ({len(merged):,} rows)")

if __name__ == "__main__":
    main()