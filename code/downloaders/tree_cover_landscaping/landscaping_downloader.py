# Download “Natural Turf Maintenance” dataset.
# Source: https://data.cityofnewyork.us/Recreation/Natural-Turf-Maintenance/tja3-yjvi

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class NaturalTurfMaintenanceDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/tja3-yjvi/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Natural Turf Maintenance"

def main():
    downloader = NaturalTurfMaintenanceDownloader()
    downloader.run()

if __name__ == "__main__":
    main()