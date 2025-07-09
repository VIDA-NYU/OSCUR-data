from code.downloaders.nyc_base_downloader import NYCDataDownloader

class SidewalkLotInfoDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/i642-2fxq/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Sidewalk Management Database - Lot Info"

def main():
    downloader = SidewalkLotInfoDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
