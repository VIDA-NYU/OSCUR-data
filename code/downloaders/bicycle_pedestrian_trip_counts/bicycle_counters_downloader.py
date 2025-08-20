# Download “Bicycle Counters” dataset.
# Source: https://data.cityofnewyork.us/Transportation/Bicycle-Counters/smn3-rzf9

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class BicycleCountersDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/smn3-rzf9/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Bicycle Counters"

def main():
    BicycleCountersDownloader().run()

if __name__ == "__main__":
    main()
