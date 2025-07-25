"""Download a sample of “MTA Subway Hourly Ridership (2020–2024)” dataset (limit=5000)
   Source: https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-2020-2024/wujg-7c2s
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class MTASubwayHourlyRidershipDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.ny.gov/api/views/wujg-7c2s/rows.csv?$accessType=DOWNLOAD"
    )
    DATASET_NAME = "MTA Subway Hourly Ridership (2020–2024) - Sample"


def main():
    MTASubwayHourlyRidershipDownloader().run()


if __name__ == "__main__":
    main()