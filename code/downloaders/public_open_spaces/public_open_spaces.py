"""
Orchestrator: Download all datasets for Multi-Use Paths (Open Streets, Open Space, and Centerlines).
"""

import argparse

from code.downloaders.public_open_spaces.open_space_downloader import (
    OpenSpaceOtherDownloader,
)
from code.downloaders.public_open_spaces.open_streets_downloader import (
    OpenStreetsDownloader,
)
from code.downloaders.public_open_spaces.street_centerline_downloader import(
    CenterlineDownloader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download NYC Open Streets, Open Space (Other), and Street Centerline (CSCL) datasets."
    )

    # ---------- output paths (editable on the CLI) ----------
    parser.add_argument(
        "--open_space_other",
        default="data/public_open_spaces/open_spaces.csv",
        help="Output path for NYC Planimetric Open Space (Other) CSV",
    )
    parser.add_argument(
        "--open_streets",
        default="data/public_open_spaces/open_streets.csv",
        help="Output path for NYC Open Streets CSV",
    )
    parser.add_argument(
        "--centerlines",
        default="data/public_open_spaces/centerlines.csv",
        help="Output path for NYC Street Centerline (CSCL) CSV",
    )

    args = parser.parse_args()

    # ---------- run each downloader ----------
    print("Downloading NYC Planimetric Open Space (Other) …")
    OpenSpaceOtherDownloader().download_csv(args.open_space_other)

    print("Downloading NYC Open Streets …")
    OpenStreetsDownloader().download_csv(args.open_streets)

    print("Downloading NYC Street Centerlines (CSCL) …")
    CenterlineDownloader().download_csv(args.centerlines)

    print("All multi-use paths datasets downloaded.")


if __name__ == "__main__":
    main()