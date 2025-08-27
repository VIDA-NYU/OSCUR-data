"""
Download “Housing Database by 2020 CDTA” dataset.
Source: https://data.cityofnewyork.us/Housing-Development/Housing-Database-by-2020-CDTA/48dt-mn3z
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class HousingDatabaseBy2020CDTADownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/resource/48dt-mn3z.csv"
    DATASET_NAME = "Housing Database by 2020 CDTA"

def main():
    HousingDatabaseBy2020CDTADownloader().run()

if __name__ == "__main__":
    main()