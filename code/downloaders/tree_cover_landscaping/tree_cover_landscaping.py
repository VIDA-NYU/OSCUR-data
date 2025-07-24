"""
Orchestrator: Download all datasets for Tree Cover & Landscaping (Turf Maintenance and Parks Zones).
"""

import argparse

from code.downloaders.tree_cover_landscaping.landscaping_downloader import (
    NaturalTurfMaintenanceDownloader,
)
from code.downloaders.tree_cover_landscaping.nyc_park_zones_downloader import (
    ParksZonesDownloader,
)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download NYC Natural Turf Maintenance and Parks Zones datasets."
    )

    # ---------- output paths ----------
    parser.add_argument(
        "--turf_maintenance",
        default="data/tree_cover_landscaping/natural_turf_maintenance.csv",
        help="Output path for Natural Turf Maintenance CSV",
    )
    parser.add_argument(
        "--parks_zones",
        default="data/tree_cover_landscaping/parks_zones.csv",
        help="Output path for NYC Park Zones CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading Natural Turf Maintenance …")
    NaturalTurfMaintenanceDownloader().download_csv(args.turf_maintenance)

    print("Downloading NYC Park Zones …")
    ParksZonesDownloader().download_csv(args.parks_zones)

    print("All datasets downloaded.")


if __name__ == "__main__":
    main()