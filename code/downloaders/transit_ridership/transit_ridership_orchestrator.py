"""
Orchestrator: Download all datasets for Transit Ridership (Subway, Bus, Ferry).
"""

import argparse

from code.downloaders.transit_ridership.mta_subway_hourly_ridership_downloader import (
    MTASubwayHourlyRidershipDownloader,
)
from code.downloaders.transit_ridership.mta_bus_hourly_ridership_downloader import (
    MTABusHourlyRidershipDownloader,
)
from code.downloaders.transit_ridership.ferry_ridership import (
    NYCFerryRidershipDownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download MTA Subway Hourly Ridership, MTA Bus Hourly Ridership, and NYC Ferry Ridership datasets."
    )

    # ---------- output paths (editable on the CLI) ----------
    parser.add_argument(
        "--subway",
        default="data/transit_ridership/mta_subway_hourly_ridership.csv",
        help="Output path for MTA Subway Hourly Ridership CSV",
    )
    parser.add_argument(
        "--bus",
        default="data/transit_ridership/mta_bus_hourly_ridership.csv",
        help="Output path for MTA Bus Hourly Ridership CSV",
    )
    parser.add_argument(
        "--ferry",
        default="data/transit_ridership/nyc_ferry_ridership.csv",
        help="Output path for NYC Ferry Ridership CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading MTA Subway Hourly Ridership …")
    MTASubwayHourlyRidershipDownloader().download_csv(args.subway)

    print("Downloading MTA Bus Hourly Ridership …")
    MTABusHourlyRidershipDownloader().download_csv(args.bus)

    print("Downloading NYC Ferry Ridership …")
    NYCFerryRidershipDownloader().download_csv(args.ferry)

    print("All transit ridership datasets downloaded.")


if __name__ == "__main__":
    main()