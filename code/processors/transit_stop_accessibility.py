#!/usr/bin/env python3
"""
Transit-Stop-Accessibility | Spatial Join Processor
────────────────────────────────────────────────────────────
Enriches ADA pedestrian-ramp points and Accessible Pedestrian-Signal (APS) points
with their **nearest NYC curb segment**.

Workflow
1. Load ramps, APS, and curb segments as GeoDataFrames (CRS: EPSG:4326).
2. Re-project all layers to EPSG:2263 (NY State Plane) for street-level accuracy.
3. `sjoin_nearest()` (≤ 15 m) to attach curb attributes + distance.
4. Convert the matched curb geometry to WGS-84 WKT.
5. Re-project the point geometry back to EPSG:4326 and export a flat CSV.

Run:
python -m code.processors.transit_stop_accessibility \
  --aps   data/transit_stop_accessibility/accessible_pedestrian_signal_locations.csv \
  --ramps data/transit_stop_accessibility/pedestrian_ramp_locations.csv \
  --curbs data/transit_stop_accessibility/nyc_curbs.csv \
  --out   data/transit_stop_accessibility/transit_stop_accessibility_merged.csv
"""

from pathlib import Path
import argparse, pandas as pd, geopandas as gpd
from shapely.wkt import loads

CRS_WGS84   = "EPSG:4326"
CRS_METRIC  = "EPSG:2263"      # NAD83 / New York Long Island (ftUS)
CURB_RADIUS = 120              # feet

# ─────────────────────────  loaders  ─────────────────────────
def load_curbs(path: Path) -> gpd.GeoDataFrame:
    """Street-segment linework from CSCL – stored in WKT lon/lat."""
    df = pd.read_csv(path, low_memory=False)
    df["geometry"] = df["the_geom"].apply(loads)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=CRS_WGS84) \
             .to_crs(CRS_METRIC)
    id_cols = [c for c in gdf.columns if "id" in c.lower()]
    return gdf[["geometry"] + id_cols]

def load_ramps(path: Path) -> gpd.GeoDataFrame:
    KEEP = {
        "RampID": "feature_id", "CornerID": "corner_id", "Borough": "borough",
        "Ramp_OnStreet": "on_street", "StName2": "cross_street",
        "DWS_CONDITIONS": "detect_warn_strip", "the_geom": "the_geom"
    }
    df = pd.read_csv(path, low_memory=False).rename(columns=KEEP)
    xy = df["the_geom"].str.extract(r"POINT\s*\(([-\d.]+)\s+([-\d.]+)\)").astype(float)
    df["lon"], df["lat"] = xy[0], xy[1]
    gdf = gpd.GeoDataFrame(
        df.drop(columns="the_geom"),
        geometry=gpd.points_from_xy(df["lon"], df["lat"]),
        crs=CRS_WGS84,
    ).to_crs(CRS_METRIC)
    gdf["source"] = "pedestrian_ramp"
    return gdf

def load_aps(path: Path) -> gpd.GeoDataFrame:
    KEEP = {
        "OBJECTID": "feature_id", "BoroName": "borough",
        "ON_STREET": "on_street", "AT_STREET": "cross_street",
        "DEVICE_STATUS": "device_status", "Date_Insta": "install_date",
        "POINT_X": "lon", "POINT_Y": "lat",
    }
    df = pd.read_csv(path, low_memory=False).rename(columns=KEEP)
    df = df.dropna(subset=["lon", "lat"]).copy()
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["lon"], df["lat"]),
        crs=CRS_WGS84,
    ).to_crs(CRS_METRIC)
    gdf["source"] = "accessible_signal"
    return gdf

# ─────────────────── helper: nearest-curb join ───────────────────
def snap_to_curb(points: gpd.GeoDataFrame,
                 curbs: gpd.GeoDataFrame,
                 max_dist: int = CURB_RADIUS) -> gpd.GeoDataFrame:

    joined = gpd.sjoin_nearest(
        points,
        curbs[["geometry"]],
        how="left",
        max_distance=max_dist,
        distance_col="dist_to_curb_ft",
    )

    joined["curb_geometry"] = None
    mask = joined["index_right"].notna()
    if mask.any():
        matched_geom = curbs.loc[
            joined.loc[mask, "index_right"].astype(int), "geometry"
        ].values
        joined.loc[mask, "curb_geometry"] = matched_geom

    joined = joined.drop(columns="index_right")
    joined = joined.set_geometry("geometry")
    return joined

# ───────────────────────────  main  ────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="Snap ramps & APS to nearest curb")
    ap.add_argument("--aps",   required=True, type=Path)
    ap.add_argument("--ramps", required=True, type=Path)
    ap.add_argument("--curbs", required=True, type=Path)
    ap.add_argument("--out",   required=True, type=Path)
    args = ap.parse_args()

    curbs  = load_curbs(args.curbs)
    ramps  = load_ramps(args.ramps)
    aps    = load_aps(args.aps)

    merged = gpd.GeoDataFrame(
        pd.concat([
            snap_to_curb(ramps, curbs),
            snap_to_curb(aps,   curbs)
        ], ignore_index=True),
        geometry="geometry",
        crs=CRS_METRIC,
    )

    merged["curb_geom_wkt"] = (
        gpd.GeoSeries(merged["curb_geometry"], crs=CRS_METRIC)
        .to_crs(CRS_WGS84)
        .apply(lambda g: g.wkt if g is not None else None)
    )

    merged = merged.to_crs(CRS_WGS84)
    merged["lon"] = merged.geometry.x
    merged["lat"] = merged.geometry.y
    merged.drop(columns=["geometry", "curb_geometry"], inplace=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(args.out, index=False)

    hits = merged["curb_geom_wkt"].notna().sum()
    print(f"✅  Saved {len(merged):,} rows → {args.out} | curb matches: {hits:,}")
    print(f"{hits/len(merged)*100:.1f}% matched")

if __name__ == "__main__":
    main()