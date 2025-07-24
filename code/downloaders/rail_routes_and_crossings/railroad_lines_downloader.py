# code/downloaders/rail_routes/railroad_lines_downloader.py

"""
Download NYC Planimetric Railroad Line dataset.
Source: https://data.cityofnewyork.us/Transportation/NYC-Planimetric-Database-Railroad-Line/anc7-97cy
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class RailroadLinesDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/anc7-97cy/rows.csv?$accessType=DOWNLOAD"
    DATASET_NAME = "NYC Planimetric Railroad Lines"

def main():
    RailroadLinesDownloader().run()

if __name__ == "__main__":
    main()