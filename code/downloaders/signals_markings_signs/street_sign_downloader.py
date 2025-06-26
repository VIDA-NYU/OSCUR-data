from code.downloaders.nyc_base_downloader import NYCDataDownloader

class StreetSignWorkOrdersDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/qt6m-xctn/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Street Sign Work Orders"

def main():
    StreetSignWorkOrdersDownloader().run()

if __name__ == "__main__":
    main()
