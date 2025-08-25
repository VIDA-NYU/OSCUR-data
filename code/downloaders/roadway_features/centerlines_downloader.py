# Download “NYC Street Centerline” dataset.
# Source: https://data.cityofnewyork.us/City-Government/Centerline/inkn-q76z

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class CenterlineDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/inkn-q76z/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "NYC Street Centerline"

def main():
    downloader = CenterlineDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
