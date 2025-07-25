"""
NYC Open Data ▸ NYC Planimetric Database - Open Space (Other)
Dataset page : https://data.cityofnewyork.us/Recreation/NYC-Planimetric-Database-Open-Space-Other-/b7j8-z8a7
CSV endpoint  : https://data.cityofnewyork.us/api/views/b7j8-z8a7/rows.csv?accessType=DOWNLOAD
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class OpenSpaceOtherDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/b7j8-z8a7/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "NYC Planimetric Database - Open Space (Other)"

def main() -> None:
    OpenSpaceOtherDownloader().run()

if __name__ == "__main__":
    main()