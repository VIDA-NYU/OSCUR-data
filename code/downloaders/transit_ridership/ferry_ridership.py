"""Download a sample of “NYC Ferry Ridership” dataset (limit=5000)
   Source: https://data.cityofnewyork.us/Transportation/NYC-Ferry-Ridership/t5n6-gx8c
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class NYCFerryRidershipDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/t5n6-gx8c/rows.csv?$accessType=DOWNLOAD"
    )
    DATASET_NAME = "NYC Ferry Ridership - Sample"


def main():
    NYCFerryRidershipDownloader().run()


if __name__ == "__main__":
    main()