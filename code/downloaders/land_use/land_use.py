"""
Main orchestrator — Land Use
Downloads all raw sources describing NYC land use, property types, and physical infrastructure.

1. Historic land uses on vacant M-zoned lots (Sanborn maps)
2. NYCHA residential addresses (public housing)
3. NYC Facilities Database (civic, academic, public service infrastructure)
4. NYC Issued Licenses (commercial activity)
5. NYC Planimetric Sidewalk geometry layer
"""

import argparse

from code.downloaders.land_use.historic_land_use_downloader import (
    HistoricLandUseDownloader,
)
from code.downloaders.land_use.nycha_residential_downloader import (
    NYCHAAddressesDownloader,
)
from code.downloaders.land_use.facilities_downloader import (
    FacilitiesDatabaseDownloader,
)
from code.downloaders.land_use.issued_licenses_downloader import (
    IssuedLicensesDownloader,
)
from code.downloaders.land_use.sidewalk_geometry_downloader import (
    SidewalkGeometryDownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download all raw sources for the Land Use data element."
    )

    # ───────── configurable output paths ─────────
    parser.add_argument(
        "--historic_land_use",
        default="data/land_use/historic_land_use.csv",
        help="Output CSV for Sanborn-based historic land uses on vacant lots",
    )
    parser.add_argument(
        "--nycha_residential",
        default="data/land_use/nycha_residential.csv",
        help="Output CSV for NYCHA residential address records",
    )
    parser.add_argument(
        "--facilities",
        default="data/land_use/facilities.csv",
        help="Output CSV for NYC Facilities Database",
    )
    parser.add_argument(
        "--issued_licenses",
        default="data/land_use/issued_licenses.csv",
        help="Output CSV for issued business licenses in NYC",
    )
    parser.add_argument(
        "--sidewalk_geom",
        default="data/land_use/sidewalks.csv",
        help="Output CSV for NYC Planimetric Sidewalk geometry layer",
    )

    args = parser.parse_args()

    # ───────── run each downloader ─────────

    print("Downloading historic land use data …")
    HistoricLandUseDownloader().download_csv(args.historic_land_use)

    print("Downloading NYCHA residential addresses …")
    NYCHAAddressesDownloader().download_csv(args.nycha_residential)

    print("Downloading NYC Facilities database …")
    FacilitiesDatabaseDownloader().download_csv(args.facilities)

    print("Downloading issued business licenses …")
    IssuedLicensesDownloader().download_csv(args.issued_licenses)

    print("Downloading NYC Planimetric Sidewalk geometry …")
    SidewalkGeometryDownloader().download_csv(args.sidewalk_geom)

    print("All land use datasets downloaded.")


if __name__ == "__main__":
    main()