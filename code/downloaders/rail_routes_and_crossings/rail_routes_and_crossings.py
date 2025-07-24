"""
Orchestrator: Download all datasets for Rail Routes and Crossings (US Rail Crossings filtered to NYC, and NYC Planimetric Railroad Lines).
"""

import argparse

from code.downloaders.rail_routes_and_crossings.crossings_downloader import RailCrossingsNYCDownloader
from code.downloaders.rail_routes_and_crossings.railroad_lines_downloader import RailroadLinesDownloader

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download Rail Routes and Crossings datasets (Rail Crossings in NYC and Planimetric Railroad Lines)."
    )

    # ---------- output paths (editable on the CLI) ----------
    parser.add_argument(
        "--rail_crossings",
        default="data/rail_routes_and_crossings/rail_crossings_nyc.csv",
        help="Output path for NYC-filtered Rail Crossings CSV",
    )
    parser.add_argument(
        "--railroad_lines",
        default="data/rail_routes_and_crossings/railroad_lines.csv",
        help="Output path for NYC Planimetric Railroad Lines CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading filtered Rail Crossings for NYC …")
    RailCrossingsNYCDownloader().download_csv(args.rail_crossings)

    print("Downloading NYC Planimetric Railroad Lines …")
    RailroadLinesDownloader().download_csv(args.railroad_lines)

    print("All rail routes and crossings datasets downloaded.")

if __name__ == "__main__":
    main()