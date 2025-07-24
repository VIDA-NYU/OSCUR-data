"""
Download “Motor Vehicle Collisions – Person” dataset.
Source: https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class MotorVehiclePersonsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/f55k-p6yu/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Motor Vehicle Collisions - Person"

def main():
    MotorVehiclePersonsDownloader().run()

if __name__ == "__main__":
    main()