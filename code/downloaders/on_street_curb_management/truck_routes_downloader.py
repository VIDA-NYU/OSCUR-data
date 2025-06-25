from code.downloaders.nyc_base_downloader import NYCDataDownloader

class TruckRoutesDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/resource/jjja-shxy.csv?$limit=50000"
    DATASET_NAME = "NYC Truck Routes"

def main():
    downloader = TruckRoutesDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
