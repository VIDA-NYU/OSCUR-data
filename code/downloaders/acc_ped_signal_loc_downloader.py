from code.downloaders.nyc_base_downloader import NYCDataDownloader

class AccessiblePedestrianSignalLocationsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/de3m-c5p4/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Accessible Pedestrian Signal Locations"

def main():
    downloader = AccessiblePedestrianSignalLocationsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()