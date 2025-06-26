from code.downloaders.signals_markings_signs.accessible_ped_signals_downloader import AccessiblePedestrianSignalsDownloader
from code.downloaders.signals_markings_signs.traffic_signal_downloader import TrafficSignal311Downloader
from code.downloaders.signals_markings_signs.street_sign_downloader import StreetSignWorkOrdersDownloader

def main():
    print("Downloading Accessible Pedestrian Signals...")
    AccessiblePedestrianSignalsDownloader().download_csv("data/signals_markings_signs/accessible_pedestrian_signals.csv")

    print("Downloading Traffic Signals...")
    TrafficSignal311Downloader().download_csv("data/signals_markings_signs/traffic_signals.csv")

    print("Downloading Street Signs...")
    StreetSignWorkOrdersDownloader().download_csv("data/signals_markings_signs/street_sign_work_orders.csv")

    print("All signals, markings, and signs data downloaded.")

if __name__ == "__main__":
    main()
