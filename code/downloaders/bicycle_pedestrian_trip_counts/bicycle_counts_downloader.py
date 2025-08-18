# Download “Bicycle Counts” dataset.
# Source: https://data.cityofnewyork.us/Transportation/Bicycle-Counts/uczf-rk3c

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class BicycleCountsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/uczf-rk3c/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Bicycle Counts"

def main():
    BicycleCountsDownloader().run()

if __name__ == "__main__":
    main()
