import argparse
from code.downloaders.on_street_curb_management.curbs_downloader import CurbsDownloader
from code.downloaders.on_street_curb_management.loading_zones_downloader import LoadingZonesDownloader
from code.downloaders.on_street_curb_management.parking_meters_downloader import ParkingMetersDownloader
from code.downloaders.on_street_curb_management.truck_routes_downloader import TruckRoutesDownloader

def main():
    parser = argparse.ArgumentParser(description="Download curb management datasets.")
    parser.add_argument("--curbs", default="data/on_street_curb_management/curbs.csv", help="Output path for curbs dataset")
    parser.add_argument("--loading_zones", default="data/on_street_curb_management/loading_zones.csv", help="Output path for loading zones dataset")
    parser.add_argument("--parking_meters", default="data/on_street_curb_management/parking_meters.csv", help="Output path for parking meters dataset")
    parser.add_argument("--truck_routes", default="data/on_street_curb_management/truck_routes.csv", help="Output path for truck routes dataset")
    args = parser.parse_args()

    print("Downloading curb segments...")
    CurbsDownloader().download_csv(args.curbs)

    print("Downloading loading zones...")
    LoadingZonesDownloader().download_csv(args.loading_zones)

    print("Downloading parking meters...")
    ParkingMetersDownloader().download_csv(args.parking_meters)

    print("Downloading truck routes...")
    TruckRoutesDownloader().download_csv(args.truck_routes)

    print("✓ All curb management data downloaded successfully.")

if __name__ == "__main__":
    main()
