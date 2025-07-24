from code.downloaders.nyc_base_downloader import NYCDataDownloader

class UrbanDesignFrontageDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/4e2n-s75z/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Urban Design and Frontage (Urban Agriculture Suitability)"

def main():
    downloader = UrbanDesignFrontageDownloader()
    downloader.run()

if __name__ == "__main__":
    main()