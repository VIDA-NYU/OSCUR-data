# Download “Vehicle Classification Counts 2011–2024” dataset.
# Source: https://data.cityofnewyork.us/Transportation/Vehicle-Classification-Counts-2011-2024-/96ay-ea4r

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class VehicleClassificationCountsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/96ay-ea4r/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Vehicle Classification Counts (2011–2024)"

def main():
    downloader = VehicleClassificationCountsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
