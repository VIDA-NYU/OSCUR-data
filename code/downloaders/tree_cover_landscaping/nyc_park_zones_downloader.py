from code.downloaders.nyc_base_downloader import NYCDataDownloader

class ParksZonesDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/4j29-i5ry/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "NYC Parks Zones"

def main():
    downloader = ParksZonesDownloader()
    downloader.run()

if __name__ == "__main__":
    main()