"""
Downloader for NYC Planimetric Database – Sidewalk layer
Source: https://data.cityofnewyork.us/City-Government/NYC-Planimetric-Database-Sidewalk/vfx9-tbb6
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader


class SidewalkGeometryDownloader(NYCDataDownloader):
    BASE_URL = (
        "https://data.cityofnewyork.us/api/views/vfx9-tbb6/rows.csv?accessType=DOWNLOAD"
    )
    DATASET_NAME = "NYC Planimetric Database - Sidewalk"


def main() -> None:
    SidewalkGeometryDownloader().run()


if __name__ == "__main__":
    main()