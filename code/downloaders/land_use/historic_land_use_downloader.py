### Historic Land Use
"""
NYC Open Data ▸ Historic Land Use Data
Dataset page : https://data.cityofnewyork.us/Environment/Historic-Land-Use-Data/r9ca-6t4q
CSV endpoint  : https://data.cityofnewyork.us/api/views/r9ca-6t4q/rows.csv?accessType=DOWNLOAD
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class HistoricLandUseDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/r9ca-6t4q/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Historic Land Use Data"

def main() -> None:
    HistoricLandUseDownloader().run()

if __name__ == "__main__":
    main()