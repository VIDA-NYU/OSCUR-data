"""
Download + convert:
Demographics and profiles at the Neighborhood Tabulation Area (NTA) level (ZIP of XLSX files)
Source page: https://data.cityofnewyork.us/City-Government/Demographics-and-profiles-at-the-Neighborhood-Tabul/kvuc-fg9b

Usage (module mode):
python -m code.downloaders.socio_demographics.nta_profiles_downloader \
  --url "https://data.cityofnewyork.us/api/accessors/kvuc-fg9b/attachments/16928157-.../download?filename=Demographics_and_profiles_at_the_Neighborhood_Tabulation_Area_(NTA)_level.zip" \
  --outdir data/socio_demographics/nta_profiles
"""

import argparse
import io
import os
from pathlib import Path
import zipfile

import pandas as pd
import requests


def download_zip_to_memory(url: str, timeout: int = 60) -> bytes:
    with requests.Session() as s:
        # follow redirects; stream not needed since we keep in memory
        r = s.get(url, timeout=timeout, allow_redirects=True)
        r.raise_for_status()
        return r.content


def extract_xlsx_and_write_csvs(zip_bytes: bytes, outdir: Path) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        for member in zf.namelist():
            if member.lower().endswith(".xlsx"):
                with zf.open(member) as f:
                    # read first (and in these files, only) worksheet
                    df = pd.read_excel(f, engine="openpyxl")
                csv_name = Path(member).with_suffix(".csv").name
                out_path = outdir / csv_name
                df.to_csv(out_path, index=False)
                written.append(out_path)
                print(f"✔ Wrote {out_path}  shape={df.shape}")
            else:
                # optionally save the README or codebook if present
                if member.lower().endswith((".txt", ".pdf", ".md")):
                    target = outdir / Path(member).name
                    with zf.open(member) as fsrc, open(target, "wb") as fdst:
                        fdst.write(fsrc.read())
                    print(f"• Saved attachment: {target}")
    return written


def main():
    ap = argparse.ArgumentParser(
        description="Download NTA Profiles ZIP (XLSX) and convert each workbook to CSV."
    )
    ap.add_argument(
        "--url",
        required=True,
        help="Direct ZIP download URL from the NYC Open Data page (right-click the blue Download button → Copy Link Address).",
    )
    ap.add_argument(
        "--outdir",
        default="data/socio_demographics/nta_profiles",
        help="Directory to write CSVs (default: data/socio_demographics/nta_profiles)",
    )
    ap.add_argument(
        "--timeout", type=int, default=60, help="HTTP timeout in seconds (default: 60)"
    )
    args = ap.parse_args()

    outdir = Path(args.outdir)
    print("⬇️  Downloading ZIP …")
    zip_bytes = download_zip_to_memory(args.url, timeout=args.timeout)

    print("🧩 Extracting XLSX and converting to CSV …")
    csv_paths = extract_xlsx_and_write_csvs(zip_bytes, outdir)

    print("\n✅ Done. CSVs written:")
    for p in csv_paths:
        print(f" - {p}")


if __name__ == "__main__":
    main()