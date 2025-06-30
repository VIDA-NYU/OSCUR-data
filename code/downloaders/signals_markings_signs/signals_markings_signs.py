"""
Main orchestrator: download all three Signals / Markings / Signs source datasets.

• Accessible Pedestrian Signals (APS)  
• Traffic Signals (311)  
• Street-Sign Work Orders
"""

import argparse

from code.downloaders.signals_markings_signs.accessible_ped_signals_downloader import (
    AccessiblePedestrianSignalsDownloader,
)
from code.downloaders.signals_markings_signs.traffic_signal_downloader import (
    TrafficSignal311Downloader,
)
from code.downloaders.signals_markings_signs.street_sign_downloader import (
    StreetSignWorkOrdersDownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download APS, traffic-signal, and street-sign datasets."
    )

    # ----- configurable output paths (with sensible defaults) -----
    parser.add_argument(
        "--aps",
        default="data/signals_markings_signs/accessible_pedestrian_signals.csv",
        help="Output path for Accessible Pedestrian Signals dataset",
    )
    parser.add_argument(
        "--traffic_signals",
        default="data/signals_markings_signs/traffic_signals.csv",
        help="Output path for Traffic Signals (311) dataset",
    )
    parser.add_argument(
        "--street_signs",
        default="data/signals_markings_signs/street_sign_work_orders.csv",
        help="Output path for Street-Sign Work-Orders dataset",
    )

    args = parser.parse_args()

    # -------------- run each downloader ----------------
    print("Downloading Accessible Pedestrian Signals …")
    AccessiblePedestrianSignalsDownloader().download_csv(args.aps)

    print("Downloading Traffic Signals (311) …")
    TrafficSignal311Downloader().download_csv(args.traffic_signals)

    print("Downloading Street-Sign Work Orders …")
    StreetSignWorkOrdersDownloader().download_csv(args.street_signs)

    print("All signals, markings, and signs data downloaded.")


if __name__ == "__main__":
    main()
