### NYCHA Residential Addresses
"""
NYC Open Data ▸ NYCHA Residential Addresses
Dataset page : https://data.cityofnewyork.us/Housing-Development/NYCHA-Residential-Addresses/3ub5-4ph8
CSV endpoint  : https://data.cityofnewyork.us/api/views/3ub5-4ph8/rows.csv?accessType=DOWNLOAD
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class NYCHAAddressesDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/3ub5-4ph8/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "NYCHA Residential Addresses"

def main() -> None:
    NYCHAAddressesDownloader().run()

if __name__ == "__main__":
    main()