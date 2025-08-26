"""
Processor | Housing Density by CDTA (units per acre & per square mile)

Inputs
------
- A CSV with CDTA polygons and a total-units column (e.g., DCP "Housing Database by 2020 CDTA").
  Expected defaults (override via CLI flags if different):
    * geometry col:  the_geom  (WKT Polygon/MultiPolygon)
    * code col:      cdta2020
    * name col:      cdtaname20
    * total units:   cenunits20

What it does
------------
1) Reads the CSV, parses WKT geometry into a GeoDataFrame (EPSG:4326).
2) Projects geometries to an equal-area CRS (default EPSG:2263 – NY State Plane feet).
3) Computes land area in acres and square miles.
4) Computes housing density:
      units_per_acre  = cenunits20 / acres
      units_per_sqmi  = cenunits20 / sq_miles
5) Adds centroids (lon/lat) for easy mapping.
6) Writes a processed CSV preserving the WKT geometry and adding area + density fields.

Run
---
python -m code.processors.housing_density \
  --input  data/housing_density/housing_by_cdta_2020.csv \
  --output data/housing_density/housing_density_cdta.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import geopandas as gpd
from shapely import wkt


def _read_wkt_csv(
    path: str,
    geom_col: str,
    crs: str = "EPSG:4326",
) -> gpd.GeoDataFrame:
    df = pd.read_csv(path, low_memory=False)
    if geom_col not in df.columns:
        raise ValueError(f"'{geom_col}' not found in {path} columns.")
    geom = df[geom_col].apply(lambda s: wkt.loads(s) if isinstance(s, str) and s.strip() else None)
    gdf = gpd.GeoDataFrame(df.copy(), geometry=geom, crs=crs)
    gdf = gdf.dropna(subset=["geometry"]).reset_index(drop=True)
    return gdf


def _compute_area_fields(gdf: gpd.GeoDataFrame, area_crs: str) -> gpd.GeoDataFrame:
    """
    Project to a linear CRS (e.g., EPSG:2263 feet), compute:
      - area_sqft -> acres, sq_miles
    """
    g_metric = gdf.to_crs(area_crs)
    # EPSG:2263 is in US feet
    area_sqft = g_metric.geometry.area
    acres = area_sqft / 43_560.0
    sq_miles = acres / 640.0
    out = gdf.copy()
    out["area_acres"] = acres.values
    out["area_sq_miles"] = sq_miles.values
    return out


def main():
    ap = argparse.ArgumentParser(description="Compute housing density (units per acre & per sq-mi) by CDTA.")
    ap.add_argument("--input", required=True, help="Input CDTA CSV (with WKT polygon geometry).")
    ap.add_argument("--output", required=True, help="Output processed CSV with density metrics.")
    ap.add_argument("--geom-col", default="the_geom", help="Geometry column name (WKT). Default: the_geom")
    ap.add_argument("--code-col", default="cdta2020", help="CDTA code column. Default: cdta2020")
    ap.add_argument("--name-col", default="cdtaname20", help="CDTA name column. Default: cdtaname20")
    ap.add_argument("--units-col", default="cenunits20", help="Total housing units column. Default: cenunits20")
    ap.add_argument(
        "--area-crs",
        default="EPSG:2263",
        help="Projected CRS for area calculation (linear feet or meters). Default: EPSG:2263 (NYSP ft).",
    )
    args = ap.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 1) Read + parse geometry
    gdf = _read_wkt_csv(args.input, geom_col=args.geom_col, crs="EPSG:4326")

    # Basic column checks
    for col in (args.code_col, args.name_col, args.units_col):
        if col not in gdf.columns:
            raise ValueError(f"'{col}' not found in input columns. Present: {list(gdf.columns)[:20]} ...")

    # Ensure numeric units
    gdf[args.units_col] = pd.to_numeric(gdf[args.units_col], errors="coerce").fillna(0)

    # 2) Area in acres & sq-mi
    gdf = _compute_area_fields(gdf, area_crs=args.area_crs)

    # Guard against zero-area polygons (rare but possible due to tiny slivers)
    gdf.loc[gdf["area_acres"] <= 0, "area_acres"] = pd.NA
    gdf.loc[gdf["area_sq_miles"] <= 0, "area_sq_miles"] = pd.NA

    # 3) Densities
    gdf["units_per_acre"] = gdf[args.units_col] / gdf["area_acres"]
    gdf["units_per_sqmi"] = gdf[args.units_col] / gdf["area_sq_miles"]

    # 4) Centroid lon/lat (for quick dot mapping)
    cent = gdf.geometry.centroid
    gdf["lon"] = cent.x
    gdf["lat"] = cent.y

    # 5) Order columns & write CSV (keep original WKT column)
    keep = [
        args.code_col,
        args.name_col,
        args.units_col,
        "area_acres",
        "area_sq_miles",
        "units_per_acre",
        "units_per_sqmi",
        "lon",
        "lat",
        args.geom_col,
    ]
    # include any other columns at the end (don’t drop useful attributes)
    others = [c for c in gdf.columns if c not in keep + ["geometry"]]
    out_df = gdf[keep + others].copy()

    out_df.to_csv(out_path, index=False)
    print(
        f"✔ Saved housing density → {out_path}  "
        f"rows={len(out_df):,}  "
        f"min_acres={out_df['area_acres'].min():.2f}  "
        f"max_acres={out_df['area_acres'].max():.2f}"
    )


if __name__ == "__main__":
    main()