"""
NY State Open Data ▸ MTA Subway Stations
Dataset page : https://data.ny.gov/Transportation/MTA-Subway-Stations/39hk-dx4f
CSV endpoint  : https://data.ny.gov/api/views/39hk-dx4f/rows.csv?accessType=DOWNLOAD
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class SubwayStationsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.ny.gov/api/views/39hk-dx4f/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "MTA Subway Stations"

def main() -> None:
    SubwayStationsDownloader().run()

if __name__ == "__main__":
    main()