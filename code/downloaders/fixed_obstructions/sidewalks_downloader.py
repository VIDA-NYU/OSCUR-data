"""Download “NYC Planimetric Database - Sidewalk” dataset.
   Source: https://data.cityofnewyork.us/City-Government/NYC-Planimetric-Database-Sidewalk/52n9-sdep
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class NYCPlanimetricSidewalkDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/52n9-sdep/rows.csv?$accessType=DOWNLOAD"
    )
    DATASET_NAME = "NYC Planimetric Sidewalks"


def main():
    NYCPlanimetricSidewalkDownloader().run()


if __name__ == "__main__":
    main()