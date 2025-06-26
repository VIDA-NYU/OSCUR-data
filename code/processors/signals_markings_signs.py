"""
Processor | Signals-Markings-Signs merger

* Merges:  Accessibility Pedestrian Signals (APS),
           Street-sign work-orders,
           311 Traffic-signal complaints
* Drops obviously redundant / low-value columns up-front
* De-duplicates *within each* source by its native ID
"""

from pathlib import Path
import pandas as pd
import geopandas as gpd

# ── Config ────────────────────────────────────────────────────────────
DATA_DIR      = Path("data/signals_markings_signs")
OUT_CSV       = DATA_DIR / "signals_signs_markings_combined.csv"
CRS_WGS84     = "EPSG:4326"

# ── Column white-lists (everything else will be discarded) ────────────
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
    """
    • Keeps only requested columns
    • Builds a GeoDataFrame on the two coordinate columns
    • De-duplicates on the first ID column
    """
    df = df.loc[:, [c for c in keep_cols if c in df.columns]].copy()

    # Coerce and drop rows without coordinates
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


# ── 1. Accessible pedestrian signals (APS) ────────────────────────────
aps   = pd.read_csv(DATA_DIR / "accessible_pedestrian_signals.csv")
g_aps = frame_to_gdf(
    aps, "POINT_X", "POINT_Y", "accessible_ped_signal",
    id_cols=["F_id", "OBJECTID"], keep_cols=APS_KEEP
)

# ── 2. Street-sign work orders ────────────────────────────────────────
ss    = pd.read_csv(DATA_DIR / "street_sign_work_orders.csv")
g_ss  = frame_to_gdf(
    ss, "sign_x_coord", "sign_y_coord", "street_sign",
    id_cols=["SIGNID", "sign_id"], keep_cols=SIGN_KEEP
)

# ── 3. 311 traffic-signal complaints (new source) ─────────────────────
ts    = pd.read_csv(DATA_DIR / "traffic_signals.csv")
g_ts  = frame_to_gdf(
    ts, "Longitude", "Latitude", "traffic_signals",
    id_cols=["Unique Key"], keep_cols=TSIG_KEEP
)

# ── Merge & export ────────────────────────────────────────────────────
merged = pd.concat([g_aps, g_ss, g_ts], ignore_index=True)

# drop the geometry before writing to plain CSV
merged.drop(columns="geometry", inplace=True)

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
merged.to_csv(OUT_CSV, index=False)

print("Merged dataset written to:", OUT_CSV)
print("- Rows:", len(merged))
