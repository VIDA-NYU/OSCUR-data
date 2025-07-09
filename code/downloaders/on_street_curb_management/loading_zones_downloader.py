from code.downloaders.nyc_base_downloader import NYCDataDownloader

class LoadingZonesDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/resource/6pjf-tf5u.csv?$limit=50000"
    DATASET_NAME = "Neighborhood Loading Zones"

def main():
    downloader = LoadingZonesDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
