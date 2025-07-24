#!/usr/bin/env python3
"""
NYC Open Data  ▸ Modified ZIP Code Tabulation Areas (MODZCTA)
Dataset page : https://data.cityofnewyork.us/Health/Modified-Zip-Code-Tabulation-Areas-MODZCTA-/pri4-ifjk
CSV endpoint  : https://data.cityofnewyork.us/api/views/pri4-ifjk/rows.csv?accessType=DOWNLOAD
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class MODZCTADownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/pri4-ifjk/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Modified ZIP Code Tabulation Areas (MODZCTA)"


def main() -> None:
    MODZCTADownloader().run()


if __name__ == "__main__":
    main()