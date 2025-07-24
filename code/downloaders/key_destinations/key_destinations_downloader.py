"""
Orchestrator: Download all datasets for Facilities and Issued Licenses.
"""

import argparse

from code.downloaders.key_destinations.nyc_facilities_downloader import (
    NYCFacilitiesDownloader,
)
from code.downloaders.key_destinations.issued_licenses_downloader import (
    IssuedLicensesDownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download NYC Facilities and Issued Licenses datasets."
    )

    # ---------- output paths (editable on the CLI) ----------
    parser.add_argument(
        "--facilities",
        default="data/facilities_and_licenses/nyc_facilities.csv",
        help="Output path for NYC Facilities Database CSV",
    )
    parser.add_argument(
        "--licenses",
        default="data/facilities_and_licenses/issued_licenses.csv",
        help="Output path for Issued Licenses CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading NYC Facilities Database …")
    NYCFacilitiesDownloader().download_csv(args.facilities)

    print("Downloading Issued Licenses Dataset …")
    IssuedLicensesDownloader().download_csv(args.licenses)

    print("All datasets downloaded.")


if __name__ == "__main__":
    main()