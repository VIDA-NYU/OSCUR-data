"""
Orchestrator: download all Signals / Markings / Signs source datasets
plus the NYC Centerline layer.
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
from code.downloaders.signals_markings_signs.street_centerline_downloader import CenterlineDownloader


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download APS, traffic-signal, street-sign, and centerline datasets."
    )

    # ---------- output paths (editable on the CLI) ----------
    parser.add_argument(
        "--aps",
        default="data/signals_markings_signs/accessible_pedestrian_signals.csv",
        help="Output path for Accessible Pedestrian Signals CSV",
    )
    parser.add_argument(
        "--traffic_signals",
        default="data/signals_markings_signs/traffic_signals.csv",
        help="Output path for Traffic-signal 311 CSV",
    )
    parser.add_argument(
        "--street_signs",
        default="data/signals_markings_signs/street_sign_work_orders.csv",
        help="Output path for Street-sign work-orders CSV",
    )
    parser.add_argument(
        "--centerline",
        default="data/nyc_centerline/centerline.csv",
        help="Output path for NYC Centerline (CSCL) CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading Accessible Pedestrian Signals …")
    AccessiblePedestrianSignalsDownloader().download_csv(args.aps)

    print("Downloading Traffic-signal 311 complaints …")
    TrafficSignal311Downloader().download_csv(args.traffic_signals)

    print("Downloading Street-sign Work Orders …")
    StreetSignWorkOrdersDownloader().download_csv(args.street_signs)

    print("Downloading NYC Centerline (CSCL) …")
    CenterlineDownloader().download_csv(args.centerline)

    print("All datasets downloaded.")


if __name__ == "__main__":
    main()
