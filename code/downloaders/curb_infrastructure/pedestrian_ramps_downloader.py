# code/downloaders/curb_infrastructure/pedestrian_ramps_downloader.py

"""
Download Pedestrian Ramp Locations dataset.
Source: https://data.cityofnewyork.us/Transportation/Pedestrian-Ramp-Locations/ufzp-rrqu
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class PedestrianRampsDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/ufzp-rrqu/rows.csv?$accessType=DOWNLOAD"
    )
    DATASET_NAME = "Pedestrian Ramp Locations"


def main():
    PedestrianRampsDownloader().run()


if __name__ == "__main__":
    main()