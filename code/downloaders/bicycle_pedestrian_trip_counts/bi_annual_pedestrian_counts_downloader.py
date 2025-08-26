# Download “Bi-Annual Pedestrian Counts” dataset.
# Source: https://data.cityofnewyork.us/Transportation/Bi-Annual-Pedestrian-Counts/cqsj-cfgu

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class BiAnnualPedestrianCountsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/cqsj-cfgu/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Bi-Annual Pedestrian Counts"

def main():
    BiAnnualPedestrianCountsDownloader().run()

if __name__ == "__main__":
    main()
