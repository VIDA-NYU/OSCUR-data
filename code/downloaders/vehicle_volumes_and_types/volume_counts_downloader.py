# Download “Automated Traffic Volume Counts” dataset.
# Source: https://data.cityofnewyork.us/Transportation/Automated-Traffic-Volume-Counts/7ym2-wayt

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class AutomatedTrafficVolumeCountsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/7ym2-wayt/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Automated Traffic Volume Counts"

def main():
    downloader = AutomatedTrafficVolumeCountsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
