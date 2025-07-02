#!/usr/bin/env python3
"""
Processor | Signals-Markings-Signs  ➜  CSCL street-segment merge
Creates a **true merged** (spatially–enriched) dataset and keeps geometry so you
can plot the result directly in GeoPandas / Folium.

Run example
------------
python code/processors/signals_markings_signs.py \
  --cscl    data/signals_markings_signs/centerline.csv \
  --aps     data/signals_markings_signs/accessible_pedestrian_signals.csv \
  --signs   data/signals_markings_signs/street_sign_work_orders.csv \
  --signals data/signals_markings_signs/traffic_signals.csv \
  --out     data/signals_markings_signs/signals_markings_signs_merged.csv
"""

from pathlib import Path
import argparse
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads

CRS_WGS84  = "EPSG:4326"
CRS_METRIC = "EPSG:2263"          # NY State Plane ft / m

# ── loaders ────────────────────────────────────────────────────────────────
def load_cscl(p: Path) -> gpd.GeoDataFrame:
    df = pd.read_csv(p, low_memory=False)
    df["geometry"] = df["the_geom"].apply(loads)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=CRS_WGS84) \
            .drop(columns=["the_geom", "index_right"], errors="ignore")
    return gdf.to_crs(CRS_METRIC)

def load_pts(p: Path, x, y, keep, *, crs=CRS_WGS84) -> gpd.GeoDataFrame:
    df = pd.read_csv(p, low_memory=False)
    df = df[[c for c in keep if c in df.columns]].copy()
    df.dropna(subset=[x, y], inplace=True)
    df[x] = pd.to_numeric(df[x], errors="coerce")
    df[y] = pd.to_numeric(df[y], errors="coerce")
    df.dropna(subset=[x, y], inplace=True)

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df[x], df[y]), crs=crs
    )
    return gdf.to_crs(CRS_METRIC)

def sjoin1(left, right, dmax, dist_col):
    """One-to-one nearest-feature join, retaining index_right for look-ups."""
    return gpd.sjoin_nearest(
        left, right,
        how="left",
        max_distance=dmax,
        distance_col=dist_col,
    )

# ── script ────────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cscl",    required=True, type=Path)
    ap.add_argument("--aps",     required=True, type=Path)
    ap.add_argument("--signs",   required=True, type=Path)
    ap.add_argument("--signals", required=True, type=Path)
    ap.add_argument("--out",     required=True, type=Path)
    args = ap.parse_args()

    # base geometry
    seg = load_cscl(args.cscl)

    # point layers
    APS_KEEP  = ["F_id", "BOROUGH", "DEVICE_STATUS", "POINT_X", "POINT_Y"]
    SIGN_KEEP = ["SIGNID", "sign_type", "sign_x_coord", "sign_y_coord"]
    SIG_KEEP  = ["Unique Key", "Created Date", "Descriptor",
                 "Latitude", "Longitude", "Status"]

    aps    = load_pts(args.aps,     "POINT_X",      "POINT_Y",      APS_KEEP)
    signs  = load_pts(args.signs,   "sign_x_coord", "sign_y_coord", SIGN_KEEP)
    signal = load_pts(args.signals, "Longitude",    "Latitude",     SIG_KEEP)

    # helper for repeated nearest-joins
    def attach(base, pts, dmax, dist_tag, prefix):
        seg_ = sjoin1(base, pts, dmax, dist_tag)

        attrs = (
            pts.drop(columns="geometry")
                .add_prefix(prefix + "_")
                .reset_index()                      # expose original index
                .rename(columns={"index": "index_right"})
        )

        seg_ = seg_.merge(attrs, on="index_right", how="left")
        return seg_.drop(columns="index_right")

    seg = attach(seg, aps,    20, "dist_aps",  "aps")
    seg = attach(seg, signs,  20, "dist_sign", "sign")
    seg = attach(seg, signal, 30, "dist_sig",  "sig")

    # keep the business columns only
    KEEP = [
        "PHYSICALID", "STATUS", "TRAFDIR", "RW_TYPE",
        "Posted Speed", "Segment Length",
        "dist_aps", "dist_sign", "dist_sig",
        "aps_F_id", "aps_BOROUGH", "aps_DEVICE_STATUS",
        "sign_SIGNID", "sign_sign_type",
        "sig_Unique Key", "sig_Created Date", "sig_Descriptor", "sig_Status"
    ]
    seg = seg[[c for c in KEEP if c in seg.columns] + ["geometry"]]

    # re-project to WGS-84 for final outputs
    seg = seg.to_crs(CRS_WGS84)

    # centroid lon / lat
    seg["lon"] = seg.geometry.centroid.x
    seg["lat"] = seg.geometry.centroid.y

    # preserve full polyline as WKT
    seg["geometry_wkt"] = seg.geometry.to_wkt()

    # for CSV: drop shapely objects, keep WKT + lon/lat
    seg.drop(columns="geometry", inplace=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    seg.to_csv(args.out, index=False)
    print(f"✓ merged file → {args.out}   rows={len(seg):,}")

if __name__ == "__main__":
    main()