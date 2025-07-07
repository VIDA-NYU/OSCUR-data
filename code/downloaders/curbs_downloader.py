from code.downloaders.nyc_base_downloader import NYCDataDownloader

class CurbsDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/5xvt-8cbk/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "NYC Planimetric Database: Curbs"

def main():
    downloader = CurbsDownloader()
    downloader.run()

if __name__ == "__main__":
    main()