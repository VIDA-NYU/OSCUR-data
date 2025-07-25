from code.downloaders.nyc_base_downloader import NYCDataDownloader

class CenterlineDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/3mf9-qshr/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "NYC Street Centerline (CSCL)"

def main():
    CenterlineDownloader().run()

if __name__ == "__main__":
    main()