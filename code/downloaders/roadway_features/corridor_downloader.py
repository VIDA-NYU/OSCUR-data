# Download “Vision Zero Safety Improvements – Corridors” dataset.
# Source: https://data.cityofnewyork.us/Transportation/VZV_SIP-Corridors/if4c-w48d

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class SafetyImprovementsCorridorsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/if4c-w48d/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Vision Zero Safety Improvements – Corridors"

def main():
    downloader = SafetyImprovementsCorridorsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
