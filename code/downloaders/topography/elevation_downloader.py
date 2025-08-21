"""
Download a sample of “NYC Elevation Points” dataset (limit=5000)
Source: https://data.cityofnewyork.us/Transportation/NYC-Planimetric-Database-Elevation-Points/9uxf-ng6q
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class NYCElevationPointsDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/9uxf-ng6q/rows.csv?$accessType=DOWNLOAD"
    )
    DATASET_NAME = "NYC Elevation Points - Sample"


def main():
    NYCElevationPointsDownloader().run()


if __name__ == "__main__":
    main()