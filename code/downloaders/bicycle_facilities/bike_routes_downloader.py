# code/downloaders/bicycle/bike_routes_downloader.py

"""
Download NYC DOT Bicycle Facilities dataset.

Source: https://data.cityofnewyork.us/dataset/New-York-City-Bike-Routes/mzxg-pwib
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class BikeRoutesDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/resource/mzxg-pwib.csv"
    DATASET_NAME = "NYC Bicycle Facilities"

def main():
    BikeRoutesDownloader().run()

if __name__ == "__main__":
    main()