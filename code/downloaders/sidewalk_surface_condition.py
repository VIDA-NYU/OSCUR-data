"""
Main orchestrator — Sidewalk-Surface-Condition
Downloads all raw sources that describe NYC sidewalk condition.

1. 311 sidewalk‐condition complaints
2. Sidewalk Violations (ECB / DOB)
3. Sidewalk Lot-info lookup (parcel context)
4. “All Tree Damage” defects from the Sidewalk Management Database
5. DOT Sidewalk Surface Condition survey
6. NYC Planimetric Sidewalk geometry layer
"""

import argparse

from code.downloaders.sidewalk_surface_condition.sidewalk_complaints_311_downloader import (
    SidewalkComplaints311Downloader,
)
from code.downloaders.sidewalk_surface_condition.sidewalk_violations_downloader import (
    SidewalkViolationsDownloader,
)
from code.downloaders.sidewalk_surface_condition.sidewalk_lot_info_downloader import (
    SidewalkLotInfoDownloader,
)
from code.downloaders.sidewalk_surface_condition.tree_damage_downloader import (
    TreeDamageDownloader,
)
from code.downloaders.sidewalk_surface_condition.sidewalk_geometry_downloader import (
    SidewalkGeometryDownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download all raw sources for the Sidewalk-Surface-Condition data element."
    )

    # ───────── configurable output paths ─────────
    parser.add_argument(
        "--complaints_311",
        default="data/sidewalk_surface_condition/sidewalk_complaints_311.csv",
        help="Output CSV for 311 sidewalk complaints",
    )
    parser.add_argument(
        "--violations",
        default="data/sidewalk_surface_condition/sidewalk_violations.csv",
        help="Output CSV for sidewalk violations (ECB / DOB)",
    )
    parser.add_argument(
        "--lot_info",
        default="data/sidewalk_surface_condition/sidewalk_lot_info.csv",
        help="Output CSV for sidewalk lot-info / parcel lookup",
    )
    parser.add_argument(
        "--tree_damage",
        default="data/sidewalk_surface_condition/tree_damage.csv",
        help="Output CSV for Sidewalk Management Database – All Tree Damage",
    )
    parser.add_argument(
        "--sidewalk_geom",
        default="data/sidewalk_surface_condition/sidewalk_planimetric.csv",
        help="Output CSV for NYC Planimetric Sidewalk geometry layer",
    )

    args = parser.parse_args()

    # ───────── run each downloader ─────────

    print("Downloading 311 sidewalk-condition complaints …")
    SidewalkComplaints311Downloader().download_csv(args.complaints_311)

    print("Downloading sidewalk violations (ECB / DOB) …")
    SidewalkViolationsDownloader().download_csv(args.violations)

    print("Downloading sidewalk lot-info lookup …")
    SidewalkLotInfoDownloader().download_csv(args.lot_info)

    print("Downloading sidewalk tree-damage records …")
    TreeDamageDownloader().download_csv(args.tree_damage)

    print("Downloading NYC Planimetric Sidewalk geometry …")
    SidewalkGeometryDownloader().download_csv(args.sidewalk_geom)

    print("All sidewalk-surface-condition datasets downloaded.")


if __name__ == "__main__":
    main()