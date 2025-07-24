"""
NYC Open Data ▸ NYC Planimetric Database - Open Space (Parks)
Dataset page : https://data.cityofnewyork.us/City-Government/NYC-Planimetric-Database-Open-Space-Parks-/g84h-jbjm
CSV endpoint  : https://data.cityofnewyork.us/api/views/g84h-jbjm/rows.csv?accessType=DOWNLOAD
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class ParksDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/y6ja-fw4f/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "NYC Planimetric Parks"

def main() -> None:
    ParksDownloader().run()

if __name__ == "__main__":
    main()