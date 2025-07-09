from code.downloaders.nyc_base_downloader import NYCDataDownloader

class PedestrianRampLocationsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/ufzp-rrqu/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Pedestrian Ramp Locations"

def main():
    downloader = PedestrianRampLocationsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
