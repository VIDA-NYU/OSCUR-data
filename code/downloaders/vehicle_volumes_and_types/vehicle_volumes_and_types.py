"""
Orchestrator: Download all datasets for Vehicle Volumes & Types (ATR counts, vehicle classification, and NYC Street Centerline).
"""

import argparse

from code.downloaders.vehicle_volumes_and_types.volume_counts_downloader import (
    AutomatedTrafficVolumeCountsDownloader,
)
from code.downloaders.vehicle_volumes_and_types.classification_counts_downloader import (
    VehicleClassificationCountsDownloader,
)
from code.downloaders.vehicle_volumes_and_types.nyc_centerlines_downloader import (
    CenterlineDownloader,
)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download NYC DOT ATR counts, Vehicle Classification Counts (2014–2019), and NYC Street Centerline."
    )

    # ---------- output paths ----------
    parser.add_argument(
        "--atr_counts",
        default="data/vehicle_volumes_and_types/automated_traffic_volume_counts.csv",
        help="Output path for Automated Traffic Volume Counts CSV",
    )
    parser.add_argument(
        "--vehicle_classification",
        default="data/vehicle_volumes_and_types/vehicle_classification_counts_2014_2019.csv",
        help="Output path for Vehicle Classification Counts (2014–2019) CSV",
    )
    parser.add_argument(
        "--centerline",
        default="data/vehicle_volumes_and_types/nyc_street_centerline.csv",
        help="Output path for NYC Street Centerline CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading Automated Traffic Volume Counts …")
    AutomatedTrafficVolumeCountsDownloader().download_csv(args.atr_counts)

    print("Downloading Vehicle Classification Counts (2014–2019) …")
    VehicleClassificationCountsDownloader().download_csv(args.vehicle_classification)

    print("Downloading NYC Street Centerline …")
    CenterlineDownloader().download_csv(args.centerline)

    print("All datasets downloaded.")


if __name__ == "__main__":
    main()
