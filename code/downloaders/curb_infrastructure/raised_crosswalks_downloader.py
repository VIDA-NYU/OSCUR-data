# code/downloaders/curb_infrastructure/raised_crosswalks_downloader.py

"""
Download Raised Crosswalk Locations dataset.
Source: https://data.cityofnewyork.us/Transportation/Raised-Crosswalk-Locations/uh2s-ftgh
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class RaisedCrosswalksDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/uh2s-ftgh/rows.csv?$accessType=DOWNLOAD"
    )
    DATASET_NAME = "Raised Crosswalk Locations"


def main():
    RaisedCrosswalksDownloader().run()


if __name__ == "__main__":
    main()