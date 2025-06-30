"""
Processor | Signals-Markings-Signs merger
* Merges:  Accessibility Pedestrian Signals (APS),
           Street-sign work-orders,
           311 Traffic-signal complaints
* Drops obviously redundant / low-value columns up-front
* De-duplicates *within each* source by its native ID
"""

import argparse
from pathlib import Path
import pandas as pd
import geopandas as gpd

CRS_WGS84 = "EPSG:4326"

# ── Column white-lists ────────────────────────────────────────────────
APS_KEEP = [
    "F_id", "OBJECTID", "BOROUGH", "ON_STREET", "AT_STREET",
    "DEVICE_STATUS", "POINT_X", "POINT_Y"
]

SIGN_KEEP = [
    "SIGNID", "sign_id", "sign_type", "borough",
    "sign_x_coord", "sign_y_coord"
]

TSIG_KEEP = [
    "Unique Key", "Created Date", "Closed Date", "Status",
    "Complaint Type", "Descriptor",
    "Latitude", "Longitude",  # geometry columns
    "Street Name", "Incident Zip", "Borough"
]

# ── Helper ────────────────────────────────────────────────────────────
def frame_to_gdf(df: pd.DataFrame,
                 x_col: str,
                 y_col: str,
                 src_name: str,
                 id_cols: list[str],
                 keep_cols: list[str]) -> gpd.GeoDataFrame:
    df = df.loc[:, [c for c in keep_cols if c in df.columns]].copy()

    df = df.dropna(subset=[x_col, y_col])
    df[x_col] = pd.to_numeric(df[x_col], errors="coerce")
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
    df = df.dropna(subset=[x_col, y_col])

    df["geometry"] = gpd.points_from_xy(df[x_col], df[y_col])
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=CRS_WGS84)
    gdf["source"] = src_name

    for col in id_cols:
        if col in gdf.columns and gdf[col].nunique() > 100:
            gdf = gdf.drop_duplicates(subset=col, keep="first")
            break
    return gdf


def main():
    parser = argparse.ArgumentParser(description="Merge APS, sign work orders, and traffic signal complaints into one CSV")
    parser.add_argument("--aps", required=True, help="Path to APS CSV")
    parser.add_argument("--signs", required=True, help="Path to street sign work orders CSV")
    parser.add_argument("--signals", required=True, help="Path to traffic signals CSV")
    parser.add_argument("--output", required=True, help="Path to save merged output CSV")
    args = parser.parse_args()

    aps_df = pd.read_csv(args.aps)
    g_aps = frame_to_gdf(
        aps_df, "POINT_X", "POINT_Y", "accessible_ped_signal",
        id_cols=["F_id", "OBJECTID"], keep_cols=APS_KEEP
    )

    signs_df = pd.read_csv(args.signs)
    g_signs = frame_to_gdf(
        signs_df, "sign_x_coord", "sign_y_coord", "street_sign",
        id_cols=["SIGNID", "sign_id"], keep_cols=SIGN_KEEP
    )

    sig_df = pd.read_csv(args.signals)
    g_sig = frame_to_gdf(
        sig_df, "Longitude", "Latitude", "traffic_signals",
        id_cols=["Unique Key"], keep_cols=TSIG_KEEP
    )

    merged = pd.concat([g_aps, g_signs, g_sig], ignore_index=True)
    merged.drop(columns="geometry", inplace=True)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(args.output, index=False)

    print("Merged dataset written to:", args.output)
    print("- Rows:", len(merged))


if __name__ == "__main__":
    main()
