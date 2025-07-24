"""
Orchestrator: Download all datasets for Transit Stops and Routes (Subway Stations, Intercity Bus Stops, Sidewalk Geometry).
"""

import argparse

from code.downloaders.transit_stops_routes.subway_stations_downloader import (
    SubwayStationsDownloader,
)
from code.downloaders.transit_stops_routes.bus_stop_permits_downloader import (
    IntercityBusStopsDownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download MTA Subway Stations and Intercity Bus Stop Permits."
    )

    # ---------- output paths (editable on the CLI) ----------
    parser.add_argument(
        "--subway_stations",
        default="data/transit_stops_routes/subway_stations.csv",
        help="Output path for MTA Subway Stations CSV",
    )
    parser.add_argument(
        "--intercity_bus_stops",
        default="data/transit_stops_routes/intercity_bus_stops.csv",
        help="Output path for Intercity Bus Stop Permits CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading MTA Subway Stations …")
    SubwayStationsDownloader().download_csv(args.subway_stations)

    print("Downloading Intercity Bus Stop Permits …")
    IntercityBusStopsDownloader().download_csv(args.intercity_bus_stops)

    print("All transit stops and routes datasets downloaded.")


if __name__ == "__main__":
    main()