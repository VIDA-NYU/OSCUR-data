"""
NYC Open Data ▸ NYC Open Streets Locations
Dataset page : https://data.cityofnewyork.us/Health/Open-Streets-Locations/uiay-nctu
CSV endpoint  : https://data.cityofnewyork.us/api/views/uiay-nctu/rows.csv?accessType=DOWNLOAD
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class OpenStreetsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/uiay-nctu/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "NYC Open Streets Locations"

def main() -> None:
    OpenStreetsDownloader().run()

if __name__ == "__main__":
    main()