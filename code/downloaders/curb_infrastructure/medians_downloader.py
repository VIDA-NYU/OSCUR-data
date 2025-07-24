
"""
Download Planimetric Medians dataset.
Source: https://data.cityofnewyork.us/Transportation/NYC-Planimetric-Database-Median/ees7-4ufv
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class MediansDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/ees7-4ufv/rows.csv?$accessType=DOWNLOAD"
    )
    DATASET_NAME = "Planimetric Medians"


def main():
    MediansDownloader().run()


if __name__ == "__main__":
    main()