"""Download a sample of “MTA Bus Hourly Ridership (2020–2024)”
   Source: https://data.ny.gov/Transportation/MTA-Bus-Hourly-Ridership-2020-2024/kv7t-n8in
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class MTABusHourlyRidershipDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.ny.gov/api/views/kv7t-n8in/rows.csv?$accessType=DOWNLOAD"
    )
    DATASET_NAME = "MTA Bus Hourly Ridership (2020–2024) - Sample"


def main():
    MTABusHourlyRidershipDownloader().run()


if __name__ == "__main__":
    main()