from code.downloaders.nyc_base_downloader import NYCDataDownloader

class TreeDamageDownloader(NYCDataDownloader):
    BASE_URL = "https://data.cityofnewyork.us/api/views/j6v2-6uxq/rows.csv?accessType=DOWNLOAD"
    DATASET_NAME = "Sidewalk Management - Tree Root Damage"

def main():
    downloader = TreeDamageDownloader()
    downloader.run()

if __name__ == "__main__":
    main()
