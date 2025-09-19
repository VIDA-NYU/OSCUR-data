"""
Download “NYC 2000 Census Tract Boundaries” dataset (CSV)
Source: https://data.cityofnewyork.us/City-Government/nyct2000/7igh-afai
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class NYC2000CensusTractsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/resource/7igh-afai.csv?$limit=3000"
    # BASE_URL = "https://data.cityofnewyork.us/api/views/7igh-afai/rows.csv?accessType=DOWNLOAD" # Use this if the above fails  
    DATASET_NAME = "NYC 2000 Census Tract Boundaries (nyct2000)"


def main():
    NYC2000CensusTractsDownloader().run()


if __name__ == "__main__":
    main()