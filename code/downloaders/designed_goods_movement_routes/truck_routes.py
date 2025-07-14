"""
Download the “New York City Truck Routes” dataset
Source: https://data.cityofnewyork.us/Transportation/New-York-City-Truck-Routes/jjja-shxy
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class NYCTruckRoutesDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/jjja-shxy/rows.csv?accessType=DOWNLOAD"
    )
    DATASET_NAME = "New York City Truck Routes"


def main() -> None:
    NYCTruckRoutesDownloader().run()


if __name__ == "__main__":
    main()
