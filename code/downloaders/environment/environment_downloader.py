"""
Orchestrator: Download all datasets for Environmental Data (Heat Vulnerability, Parks, Open Space, ZIP Code Geometries).
"""

import argparse

from code.downloaders.environment.heat_vulnerability_downloader import (
    HeatVulnerabilityDownloader,
)
from code.downloaders.environment.parks_downloader import (
    ParksDownloader,
)
from code.downloaders.environment.open_space_downloader import (
    OpenSpaceDownloader,
)
from code.downloaders.environment.zipcode_geom_downloader import (
    MODZCTADownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download NYC Heat Vulnerability Index, Parks, Open Space, and MODZCTA datasets."
    )

    # ---------- output paths (editable on the CLI) ----------
    parser.add_argument(
        "--heat_vulnerability",
        default="data/environment/heat_vulnerability.csv",
        help="Output path for NYC Heat Vulnerability Index CSV",
    )
    parser.add_argument(
        "--parks",
        default="data/environment/parks.csv",
        help="Output path for NYC Parks Locations CSV",
    )
    parser.add_argument(
        "--open_space",
        default="data/environment/open_space.csv",
        help="Output path for NYC Open Space (Other) CSV",
    )
    parser.add_argument(
        "--zipcode_geom",
        default="data/environment/zipcode_geom.csv",
        help="Output path for NYC Modified ZIP Code Tabulation Areas (MODZCTA) CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading NYC Heat Vulnerability Index …")
    HeatVulnerabilityDownloader().download_csv(args.heat_vulnerability)

    print("Downloading NYC Parks Locations …")
    ParksDownloader().download_csv(args.parks)

    print("Downloading NYC Open Space (Other) …")
    OpenSpaceDownloader().download_csv(args.open_space)

    print("Downloading NYC MODZCTA (ZIP Code Geometries) …")
    MODZCTADownloader().download_csv(args.zipcode_geom)

    print("All datasets downloaded.")


if __name__ == "__main__":
    main()