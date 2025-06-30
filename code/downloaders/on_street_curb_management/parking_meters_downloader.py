from code.downloaders.nyc_base_downloader import NYCDataDownloader

class ParkingMetersDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/693u-uax6/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Parking Meters - Locations and Status"

def main():
    downloader = ParkingMetersDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
