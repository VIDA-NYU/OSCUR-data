#!/usr/bin/env python3
"""
Merge geocoded sidewalk violations/tree-damage with 311 sidewalk complaints,
snapping every record to the curb edge of the nearest sidewalk polygon.
"""

from pathlib import Path
from typing import Optional, Tuple, Union
import argparse, pandas as pd, geopandas as gpd
from shapely.wkt import loads
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import nearest_points

CRS_WGS84, CRS_METRIC = "EPSG:4326", "EPSG:2263"

# ───────────────────────── helpers ──────────────────────────
def polygon_to_edge_point(poly: Union[Polygon, MultiPolygon]) -> Point:
    """Point on polygon exterior closest to centroid."""
    return next(nearest_points(poly.centroid, poly.exterior))

def pick_lon_lat(df: pd.DataFrame) -> Tuple[Optional[str], Optional[str]]:
    cols = [c.lower() for c in df.columns]
    if "longitude" in cols and "latitude" in cols:
        lon = df.columns[cols.index("longitude")]
        lat = df.columns[cols.index("latitude")]
        return lon, lat
    lon = next((df.columns[i] for i, c in enumerate(cols) if c.startswith("lon")), None)
    lat = next((df.columns[i] for i, c in enumerate(cols) if c.startswith("lat")), None)
    return lon, lat

def to_point_gdf(df: pd.DataFrame,
                 layer_name: str) -> gpd.GeoDataFrame:
    """Return GeoDataFrame in EPSG 2263, converting lon/lat or polygon → point."""
    df = df.rename(columns=str.strip)
    lon_col, lat_col = pick_lon_lat(df)

    if lon_col and lat_col:
        df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")
        df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
        df = df.dropna(subset=[lon_col, lat_col])
        gdf = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=CRS_WGS84
        )
    elif {"geometry", "the_geom"} & set(df.columns):
        geom_col = "geometry" if "geometry" in df.columns else "the_geom"
        df[geom_col] = df[geom_col].apply(loads)
        gdf = gpd.GeoDataFrame(df, geometry=geom_col, crs=CRS_WGS84)
        # convert polygon -> edge point
        gdf["geometry"] = gdf["geometry"].apply(
            lambda g: polygon_to_edge_point(g) if g.geom_type in {"Polygon", "MultiPolygon"} else g
        )
        gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty]
    else:
        raise ValueError(f"{layer_name}: no lon/lat or geometry column")

    return gdf.to_crs(CRS_METRIC)

def snap_and_shift(points: gpd.GeoDataFrame,
                   sidewalks: gpd.GeoDataFrame,
                   max_dist: Optional[float],
                   force_match: bool) -> gpd.GeoDataFrame:
    """
    Spatial join + move point to sidewalk edge.
    • If force_match=True the join runs without max_dist (guaranteed match).
    """
    joined = gpd.sjoin_nearest(
        points,
        sidewalks[["geometry"]],
        how="left",
        max_distance=max_dist if not force_match else None,
        distance_col="dist_to_sidewalk_m",
    )

    sid_poly = joined.pop("index_right").map(sidewalks.geometry)
    joined["sidewalk_geometry"] = sid_poly

    has_match = sid_poly.notna()
    joined.loc[has_match, "geometry"] = [
        nearest_points(pt, poly)[1] for pt, poly in
        zip(joined.loc[has_match, "geometry"], sid_poly[has_match])
    ]
    return joined

# ─────────────────────────── main ───────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--geocoded",       "-g", required=True, type=Path)
    ap.add_argument("--complaints_311", "-c", required=True, type=Path)
    ap.add_argument("--sidewalk_geom",  "-s", required=True, type=Path)
    ap.add_argument("--out",            "-o", required=True, type=Path)
    ap.add_argument("--snap_dist",      default=5.0, type=float,
                    help="Snap radius for 311 points (m); geocoded points always match nearest sidewalk.")
    args = ap.parse_args()

    # load sidewalks
    poly_df = pd.read_csv(args.sidewalk_geom, low_memory=False)
    if "the_geom" in poly_df.columns:
        poly_df["geometry"] = poly_df["the_geom"].apply(loads)
    sidewalks = gpd.GeoDataFrame(poly_df, geometry="geometry", crs=CRS_WGS84).to_crs(CRS_METRIC)

    # load records
    geo_pts  = to_point_gdf(pd.read_csv(args.geocoded,       low_memory=False), "geocoded")
    c311_pts = to_point_gdf(pd.read_csv(args.complaints_311, low_memory=False), "311")

    geo_pts["merged_source"]  = "violation"
    c311_pts["merged_source"] = "311_complaint"

    merged = pd.concat(
        [
            snap_and_shift(geo_pts,  sidewalks, max_dist=None,          force_match=True),
            snap_and_shift(c311_pts, sidewalks, max_dist=args.snap_dist, force_match=False),
        ],
        ignore_index=True,
    ).to_crs(CRS_WGS84)

    merged["lon"] = merged.geometry.x
    merged["lat"] = merged.geometry.y
    merged["sidewalk_geom_wkt"] = (
        gpd.GeoSeries(merged["sidewalk_geometry"], crs=CRS_METRIC)
        .to_crs(CRS_WGS84)
        .apply(lambda g: g.wkt if g is not None else None)
    )

    # essential + high-value columns
    keep_extra = [
        "ViolationID", "ViolationId", "Descriptor", "Complaint Type",
        "Created Date", "Closed Date", "bblid", "street"
    ]
    cols_out = ["merged_source", "lon", "lat",
                "dist_to_sidewalk_m", "sidewalk_geom_wkt"] + \
               [c for c in keep_extra if c in merged.columns]

    final = merged[cols_out].drop_duplicates(subset=["lon", "lat"])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(args.out, index=False)
    print(f"Saved {len(final):,} rows → {args.out}")

if __name__ == "__main__":
    main()