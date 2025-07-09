from code.downloaders.nyc_base_downloader import NYCDataDownloader

class SidewalkComplaints311Downloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/huz9-8jhi/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "311 Curb and Sidewalk Complaints"

def main():
    downloader = SidewalkComplaints311Downloader()
    downloader.run()

if __name__ == "__main__":
    main()