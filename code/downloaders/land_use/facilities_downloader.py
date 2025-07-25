### NYC Facilities Database
"""
NYC Open Data ▸ Facilities Database
Dataset page : https://data.cityofnewyork.us/City-Government/Facilities-Database/ji82-xba5
CSV endpoint  : https://data.cityofnewyork.us/api/views/ji82-xba5/rows.csv?accessType=DOWNLOAD
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class FacilitiesDatabaseDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/ji82-xba5/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Facilities Database"

def main() -> None:
    FacilitiesDatabaseDownloader().run()

if __name__ == "__main__":
    main()