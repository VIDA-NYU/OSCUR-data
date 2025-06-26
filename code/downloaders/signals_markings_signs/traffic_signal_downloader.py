from code.downloaders.nyc_base_downloader import NYCDataDownloader


class TrafficSignal311Downloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/jwvp-gyiq/rows.csv?accessType=DOWNLOAD"
    )
    DATASET_NAME = "311 Street-Light & Traffic-Signal Service Requests"


def main() -> None:
    TrafficSignal311Downloader().run()


if __name__ == "__main__":
    main()