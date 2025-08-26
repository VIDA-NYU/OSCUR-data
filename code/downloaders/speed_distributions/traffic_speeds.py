"""
Download a ~1GB sample of “DOT Traffic Speeds (NBE)” dataset (limit=1,000,000)
Source: https://data.cityofnewyork.us/Transportation/DOT-Traffic-Speeds-NBE/i4gi-tjb9
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class DOTTrafficSpeedsSampleDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/resource/i4gi-tjb9.csv?$order=data_as_of DESC&$limit=1000000"
    DATASET_NAME = "DOT Traffic Speeds (NBE) - ~1GB Sample"


def main():
    DOTTrafficSpeedsSampleDownloader().run()


if __name__ == "__main__":
    main()
