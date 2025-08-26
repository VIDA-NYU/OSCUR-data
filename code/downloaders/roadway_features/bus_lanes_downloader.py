# Download “Bus Lanes (Local Streets)” dataset.
# Source: https://data.cityofnewyork.us/Transportation/Bus-Lanes-Local-Streets/ycrg-ses3

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class BusLanesDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/ycrg-ses3/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Bus Lanes (Local Streets)"

def main():
    downloader = BusLanesDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
