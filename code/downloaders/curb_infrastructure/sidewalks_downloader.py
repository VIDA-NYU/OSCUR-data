# code/downloaders/curb_infrastructure/sidewalks_downloader.py

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