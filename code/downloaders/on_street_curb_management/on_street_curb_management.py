from code.downloaders.on_street_curb_management.curbs_downloader import CurbsDownloader
from code.downloaders.on_street_curb_management.loading_zones_downloader import LoadingZonesDownloader
from code.downloaders.on_street_curb_management.parking_meters_downloader import ParkingMetersDownloader
from code.downloaders.on_street_curb_management.truck_routes_downloader import TruckRoutesDownloader

def main():
    print("Downloading curb segments...")
    CurbsDownloader()

    print("Downloading loading zones...")
    LoadingZonesDownloader()

    print("Downloading parking meters...")
    ParkingMetersDownloader()

    print("Downloading truck routes...")
    TruckRoutesDownloader()

    print("✓ All curb management data downloaded successfully.")

if __name__ == "__main__":
    main()