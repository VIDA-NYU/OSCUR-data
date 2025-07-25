"""
Orchestrator: Download all datasets for Fixed Obstructions (Poles, Street Signs, Sidewalks).
"""

import argparse

from code.downloaders.fixed_obstructions.utility_poles_downloader import (
    TelecomFranchisePoleDownloader,
)
from code.downloaders.fixed_obstructions.signposts_downloader import (
    StreetSignWorkOrdersDownloader,
)
from code.downloaders.fixed_obstructions.sidewalks_downloader import (
    NYCPlanimetricSidewalkDownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download Mobile Telecommunications Poles, Street Sign Work Orders, and Sidewalk datasets."
    )

    # ---------- output paths (editable on the CLI) ----------
    parser.add_argument(
        "--telecom_poles",
        default="data/fixed_obstructions/telecom_franchise_poles.csv",
        help="Output path for Mobile Telecommunications Franchise Poles CSV",
    )
    parser.add_argument(
        "--street_signs",
        default="data/fixed_obstructions/street_sign_work_orders.csv",
        help="Output path for Street Sign Work Orders CSV",
    )
    parser.add_argument(
        "--sidewalks",
        default="data/fixed_obstructions/sidewalks.csv",
        help="Output path for NYC Planimetric Sidewalks CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading Mobile Telecommunications Franchise Poles …")
    TelecomFranchisePoleDownloader().download_csv(args.telecom_poles)

    print("Downloading Street Sign Work Orders …")
    StreetSignWorkOrdersDownloader().download_csv(args.street_signs)

    print("Downloading NYC Planimetric Sidewalks …")
    NYCPlanimetricSidewalkDownloader().download_csv(args.sidewalks)

    print("All fixed obstructions datasets downloaded.")


if __name__ == "__main__":
    main()