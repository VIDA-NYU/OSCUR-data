"""
Orchestrator: Download all datasets for Roadway Features
(Centerlines, Intersections Safety Improvements, Corridors Safety Improvements,
Bus Lanes, and Block Face Tree Census).
"""

import argparse

from code.downloaders.roadway_features.centerlines_downloader import CenterlineDownloader
from code.downloaders.roadway_features.intersections_downloader import SafetyImprovementsIntersectionsDownloader
from code.downloaders.roadway_features.corridor_downloader import SafetyImprovementsCorridorsDownloader
from code.downloaders.roadway_features.bus_lanes_downloader import BusLanesDownloader
from code.downloaders.roadway_features.block_face_downloader import TreeCensusBlockfaceDownloader

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download Roadway Features datasets (Centerlines, Safety Improvements, Bus Lanes, Block Face)."
    )

    # ---------- output paths (editable on the CLI) ----------
    parser.add_argument(
        "--centerlines",
        default="data/roadway_features/centerlines.csv",
        help="Output path for NYC Street Centerlines CSV",
    )
    parser.add_argument(
        "--intersections",
        default="data/roadway_features/intersections.csv",
        help="Output path for Vision Zero Safety Improvements – Intersections CSV",
    )
    parser.add_argument(
        "--corridors",
        default="data/roadway_features/corridors.csv",
        help="Output path for Vision Zero Safety Improvements – Corridors CSV",
    )
    parser.add_argument(
        "--bus_lanes",
        default="data/roadway_features/bus_lanes.csv",
        help="Output path for Bus Lanes (Local Streets) CSV",
    )
    parser.add_argument(
        "--block_face",
        default="data/roadway_features/block_face.csv",
        help="Output path for 2015 Street Tree Census – Blockface CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading NYC Street Centerlines …")
    CenterlineDownloader().download_csv(args.centerlines)

    print("Downloading Vision Zero Safety Improvements – Intersections …")
    SafetyImprovementsIntersectionsDownloader().download_csv(args.intersections)

    print("Downloading Vision Zero Safety Improvements – Corridors …")
    SafetyImprovementsCorridorsDownloader().download_csv(args.corridors)

    print("Downloading Bus Lanes (Local Streets) …")
    BusLanesDownloader().download_csv(args.bus_lanes)

    print("Downloading 2015 Street Tree Census – Blockface …")
    TreeCensusBlockfaceDownloader().download_csv(args.block_face)

    print("All roadway features datasets downloaded.")

if __name__ == "__main__":
    main()
