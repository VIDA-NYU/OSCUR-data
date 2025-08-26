# Download “2015 Street Tree Census – Blockface Data” dataset.
# Source: https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Blockface-Data/ju3b-rwpy

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class TreeCensusBlockfaceDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/ju3b-rwpy/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "2015 Street Tree Census – Blockface Data"

def main():
    downloader = TreeCensusBlockfaceDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
