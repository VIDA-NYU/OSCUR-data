"""
Orchestrator: Download all datasets for Motor Vehicle Collisions (Crashes and Persons).
Supports injury severity and safety analysis in NYC.
"""

import argparse

from code.downloaders.injuries.motor_vehicle_persons_downloader import (
    MotorVehiclePersonsDownloader,
)
from code.downloaders.injuries.motor_vehicle_crashes_downloader import (
    MotorVehicleCrashesDownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download Motor Vehicle Collisions datasets (Crashes and Persons)."
    )

    # ---------- output paths ----------
    parser.add_argument(
        "--persons",
        default="data/injuries/motor_vehicle_persons.csv",
        help="Output path for Motor Vehicle Collisions - Persons CSV",
    )
    parser.add_argument(
        "--crashes",
        default="data/injuries/motor_vehicle_crashes.csv",
        help="Output path for Motor Vehicle Collisions - Crashes CSV",
    )

    args = parser.parse_args()

    # ---------- download executions ----------
    print("Downloading Motor Vehicle Collision - Persons records …")
    MotorVehiclePersonsDownloader().download_csv(args.persons)

    print("Downloading Motor Vehicle Collision - Crashes records …")
    MotorVehicleCrashesDownloader().download_csv(args.crashes)

    print("All injury-related datasets downloaded.")


if __name__ == "__main__":
    main()