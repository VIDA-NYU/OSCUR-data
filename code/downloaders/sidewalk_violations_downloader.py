from code.downloaders.nyc_base_downloader import NYCDataDownloader

class SidewalkViolationsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/6kbp-uz6m/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Sidewalk Management Database - Violations"

def main():
    downloader = SidewalkViolationsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()