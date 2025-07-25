"""
Orchestrator: Download all datasets for Curb Infrastructure (Sidewalks, Curb Ramps, Raised Crosswalks, and Medians).
"""

import argparse

from code.downloaders.curb_infrastructure.sidewalks_downloader import NYCPlanimetricSidewalkDownloader
from code.downloaders.curb_infrastructure.pedestrian_ramps_downloader import PedestrianRampsDownloader
from code.downloaders.curb_infrastructure.raised_crosswalks_downloader import RaisedCrosswalksDownloader
from code.downloaders.curb_infrastructure.medians_downloader import MediansDownloader

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download NYC Curb Infrastructure datasets (Sidewalks, Curb Ramps, Raised Crosswalks, Medians)."
    )

    # ---------- output paths (editable on the CLI) ----------
    parser.add_argument(
        "--sidewalks",
        default="data/curb_infrastructure/sidewalks.csv",
        help="Output path for NYC Planimetric Sidewalks CSV",
    )
    parser.add_argument(
        "--pedestrian_ramps",
        default="data/curb_infrastructure/pedestrian_ramps.csv",
        help="Output path for NYC Pedestrian Ramp Locations CSV",
    )
    parser.add_argument(
        "--raised_crosswalks",
        default="data/curb_infrastructure/raised_crosswalks.csv",
        help="Output path for NYC Raised Crosswalk Locations CSV",
    )
    parser.add_argument(
        "--medians",
        default="data/curb_infrastructure/medians.csv",
        help="Output path for NYC Planimetric Medians CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading NYC Planimetric Sidewalks …")
    NYCPlanimetricSidewalkDownloader().download_csv(args.sidewalks)

    print("Downloading NYC Pedestrian Ramps …")
    PedestrianRampsDownloader().download_csv(args.pedestrian_ramps)

    print("Downloading NYC Raised Crosswalks …")
    RaisedCrosswalksDownloader().download_csv(args.raised_crosswalks)

    print("Downloading NYC Planimetric Medians …")
    MediansDownloader().download_csv(args.medians)

    print("All curb infrastructure datasets downloaded.")

if __name__ == "__main__":
    main()