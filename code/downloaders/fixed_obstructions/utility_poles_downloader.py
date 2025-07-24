"""Download “Mobile Telecommunications Franchise Pole Reservations” dataset.
   Source: https://data.cityofnewyork.us/City-Government/Mobile-Telecommunications-Franchise-Pole-Reservati/tbgj-tdd6
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class TelecomFranchisePoleDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/tbgj-tdd6/rows.csv?$accessType=DOWNLOAD"
    )
    DATASET_NAME = "Mobile Telecommunications Franchise Pole Reservations"


def main():
    TelecomFranchisePoleDownloader().run()


if __name__ == "__main__":
    main()