"""
NYC Open Data ▸ Issued Licenses Dataset
Dataset page : https://data.cityofnewyork.us/Business/Issued-Licenses/w7w3-xahh
CSV endpoint : https://data.cityofnewyork.us/api/views/w7w3-xahh/rows.csv?accessType=DOWNLOAD
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class IssuedLicensesDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/w7w3-xahh/rows.csv?accessType=DOWNLOAD"
    )
    DATASET_NAME = "Issued Licenses Dataset"


def main() -> None:
    IssuedLicensesDownloader().run()


if __name__ == "__main__":
    main()