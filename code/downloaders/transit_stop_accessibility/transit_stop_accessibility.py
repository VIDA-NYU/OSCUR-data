"""
Main orchestrator — Transit-Stop-Accessibility
Downloads the three source datasets:

1. Accessible Pedestrian Signal (APS) locations
2. Pedestrian-ramp locations
3. NYC Planimetric Curbs layer

Example run:
python -m code.downloaders.transit_stop_accessibility.transit_stop_accessibility \
  --aps   data/transit_stop_accessibility/acc_ped_signal_loc.csv \
  --ramps data/transit_stop_accessibility/ped_ramp_loc.csv \
  --curbs data/transit_stop_accessibility/curbs.csv
"""

import argparse

from code.downloaders.transit_stop_accessibility.acc_ped_signal_loc_downloader import (
    AccessiblePedestrianSignalLocationsDownloader,
)
from code.downloaders.transit_stop_accessibility.ped_ramp_locations_downloader import (
    PedestrianRampLocationsDownloader,
)
from code.downloaders.transit_stop_accessibility.curbs_downloader import (
    CurbsDownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download APS, pedestrian-ramp, and curb location datasets."
    )

    # ---------- configurable output paths ----------
    parser.add_argument(
        "--aps",
        default="data/transit_stop_accessibility/accessible_ped_signal_locations.csv",
        help="Output path for Accessible Pedestrian Signal locations CSV",
    )
    parser.add_argument(
        "--ramps",
        default="data/transit_stop_accessibility/pedestrian_ramp_locations.csv",
        help="Output path for pedestrian-ramp locations CSV",
    )
    parser.add_argument(
        "--curbs",
        default="data/transit_stop_accessibility/curbs.csv",
        help="Output path for NYC Planimetric Curbs CSV",
    )

    args = parser.parse_args()

    # ---------------- run each downloader ----------------
    print("Downloading Accessible Pedestrian Signal locations …")
    AccessiblePedestrianSignalLocationsDownloader().download_csv(args.aps)

    print("Downloading pedestrian-ramp locations …")
    PedestrianRampLocationsDownloader().download_csv(args.ramps)

    print("Downloading NYC Planimetric Curbs layer …")
    CurbsDownloader().download_csv(args.curbs)

    print("All transit-stop-accessibility data downloaded.")


if __name__ == "__main__":
    main()
