"""
NYC Open Data ▸ Intercity Bus Stop Permits
Dataset page : https://data.cityofnewyork.us/Transportation/Intercity-Bus-Stop-Permits/nmue-7zq2
CSV endpoint  : https://data.cityofnewyork.us/api/views/nmue-7zq2/rows.csv?accessType=DOWNLOAD
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class IntercityBusStopsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/nmue-7zq2/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Intercity Bus Stop Permits"

def main() -> None:
    IntercityBusStopsDownloader().run()

if __name__ == "__main__":
    main()