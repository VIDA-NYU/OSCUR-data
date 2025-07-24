"""
Download “Motor Vehicle Collisions – Crashes” dataset.
Source: https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class MotorVehicleCrashesDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Motor Vehicle Collisions - Crashes"

def main():
    MotorVehicleCrashesDownloader().run()

if __name__ == "__main__":
    main()