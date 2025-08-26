# Download “Vision Zero Safety Improvements – Intersections” dataset.
# Source: https://data.cityofnewyork.us/Transportation/VZV_SIP-Intersections/shr7-eqdc

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class SafetyImprovementsIntersectionsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/shr7-eqdc/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Vision Zero Safety Improvements – Intersections"

def main():
    downloader = SafetyImprovementsIntersectionsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
