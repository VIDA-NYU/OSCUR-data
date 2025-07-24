# code/downloaders/rail_routes/rail_crossings_downloader.py

"""
Download Rail Crossings dataset (filtered to NYC only).
Source: https://datahub.transportation.gov/Railroads/Rail-Crossings/bxx9-8s38
"""
from code.downloaders.nyc_base_downloader import NYCDataDownloader

class RailCrossingsNYCDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://datahub.transportation.gov/resource/bxx9-8s38.csv?"
        "$where=CITYNAME in("
        "'NEW YORK -BRONX',"
        "'NEW YORK-KINGS',"
        "'NEW YORK NEW YORK',"
        "'NEW YORK -QUEENS',"
        "'NEW YORK -RICHMOND'"
        ")"
    )
    DATASET_NAME = "Rail Crossings (NYC Only)"

def main():
    RailCrossingsNYCDownloader().run()

if __name__ == "__main__":
    main()