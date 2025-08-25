# Download “Vision Zero Leading Pedestrian Intervals” dataset.
# Source: https://data.cityofnewyork.us/Transportation/VZV_Leading-Pedestrian-Intervals/xc4v-ntf4

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class LeadingPedestrianIntervalsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/xc4v-ntf4/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Vision Zero Leading Pedestrian Intervals"

def main():
    downloader = LeadingPedestrianIntervalsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
