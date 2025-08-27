"""
Download “Final Disadvantaged Communities (DAC 2023)” dataset.
Source: https://data.ny.gov/Energy-Environment/Final-Disadvantaged-Communities-DAC-2023/2e6c-s6fp
"""

from code.downloaders.nyc_base_downloader import NYCDataDownloader

class DAC2023Downloader(NYCDataDownloader):
    BASE_URL = "https://data.ny.gov/api/views/2e6c-s6fp/rows.csv?$accessType=DOWNLOAD"
    DATASET_NAME = "NYS Disadvantaged Communities (DAC 2023)"

def main():
    DAC2023Downloader().run()

if __name__ == "__main__":
    main()