"""
Processor | Environmental Justice / Disadvantaged Communities → NYC Filter

What it does:
------------
1) Reads the DAC CSV.
2) Keeps only rows where the `REDC` column equals "New York City".
3) Writes the result to CSV (keeps all original columns).

Example:
--------
python -m code.processors.ej_nyc_filter \
  --input data/environmental_justice/dac_2023.csv \
  --output data/environmental_justice/processed/dac_2023_nyc_final.csv
"""

from __future__ import annotations
import argparse
import pandas as pd
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description="Filter DAC dataset to keep only NYC (REDC == 'New York City').")
    ap.add_argument("--input", required=True, help="Path to input CSV")
    ap.add_argument("--output", required=True, help="Path to save filtered NYC CSV")
    args = ap.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Load
    df = pd.read_csv(args.input, low_memory=False)

    # Filter
    filtered = df[df["REDC"].astype(str).str.strip().eq("New York City")].copy()

    # Save
    filtered.to_csv(out_path, index=False)
    print(f"✔ Saved NYC-only DAC file → {out_path}  rows={len(filtered):,}  cols={len(filtered.columns):,}")


if __name__ == "__main__":
    main()