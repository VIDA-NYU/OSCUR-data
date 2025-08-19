"""
Download the “New York City Community Health Survey” dataset
Source: https://data.cityofnewyork.us/Health/New-York-City-Community-Health-Survey/csut-3wpr
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class CommunityHealthSurveyDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/csut-3wpr/rows.csv?$accessType=DOWNLOAD"
    )
    DATASET_NAME = "NYC Community Health Survey"


def main():
    CommunityHealthSurveyDownloader().run()


if __name__ == "__main__":
    main()
