"""
Orchestrator: Download all datasets for Bicycle & Pedestrian Counts
(Bi-Annual Pedestrian Counts, Bicycle Counts, and Bicycle Counters).
"""

import argparse

from code.downloaders.bicycle_pedestrian_trip_counts.bi_annual_pedestrian_counts_downloader import (
    BiAnnualPedestrianCountsDownloader,
)
from code.downloaders.bicycle_pedestrian_trip_counts.bicycle_counts_downloader import (
    BicycleCountsDownloader,
)
from code.downloaders.bicycle_pedestrian_trip_counts.bicycle_counters_downloader import (
    BicycleCountersDownloader,
)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download NYC Bi-Annual Pedestrian Counts, Bicycle Counts, and Bicycle Counters datasets."
    )

    # ---------- output paths ----------
    parser.add_argument(
        "--ped_counts",
        default="data/bicycle_pedestrian_counts/bi_annual_pedestrian_counts.csv",
        help="Output path for Bi-Annual Pedestrian Counts CSV",
    )
    parser.add_argument(
        "--bicycle_counts",
        default="data/bicycle_pedestrian_counts/bicycle_counts.csv",
        help="Output path for Bicycle Counts CSV",
    )
    parser.add_argument(
        "--bicycle_counters",
        default="data/bicycle_pedestrian_counts/bicycle_counters.csv",
        help="Output path for Bicycle Counters CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading Bi-Annual Pedestrian Counts …")
    BiAnnualPedestrianCountsDownloader().download_csv(args.ped_counts)

    print("Downloading Bicycle Counts …")
    BicycleCountsDownloader().download_csv(args.bicycle_counts)

    print("Downloading Bicycle Counters …")
    BicycleCountersDownloader().download_csv(args.bicycle_counters)

    print("All datasets downloaded.")

if __name__ == "__main__":
    main()
