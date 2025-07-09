#!/usr/bin/env python3
"""
Concatenate sidewalk violation & tree-damage datasets
─────────────────────────────────────────────────────
Adds lot-info to each source (via BBL) and concatenates the two tables.
"""

from pathlib import Path
import argparse, pandas as pd

# ───────── helper: detect & rename BBL column ─────────
def normalise_bbl(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()
    for col in df.columns:
        if col.lower().startswith(("bblid", "borough, block and lot")):
            df = df.rename(columns={col: "bblid"})
            break
    return df

# ─────────── main ───────────
def main() -> None:
    ap = argparse.ArgumentParser(description="Concat violations & tree-damage with lot-info")
    ap.add_argument("--violations",   required=True, type=Path, help="CSV of sidewalk violations")
    ap.add_argument("--tree_damage",  required=True, type=Path, help="CSV of tree-root damage records")
    ap.add_argument("--lot_info",     required=True, type=Path, help="CSV of lot-info lookup (BBL + location)")
    ap.add_argument("--out",          required=True, type=Path, help="Output CSV path")
    args = ap.parse_args()

    # 1 ▸ load
    viol = normalise_bbl(pd.read_csv(args.violations,  dtype=str, low_memory=False))
    tree = normalise_bbl(pd.read_csv(args.tree_damage, dtype=str, low_memory=False))
    lot  = normalise_bbl(pd.read_csv(args.lot_info,    dtype=str, low_memory=False))

    if "bblid" not in viol.columns or "bblid" not in lot.columns:
        raise ValueError("No BBL column found in violations or lot-info")

    # 2 ▸ enrich each dataset with lot-info
    viol_en = viol.merge(lot, how="left", on="bblid")
    viol_en["source"] = "violation"

    tree_en = (
        tree.merge(lot, how="left", on="bblid") if "bblid" in tree.columns else tree
    )
    tree_en["source"] = "tree_root_damage"

    # 3 ▸ concatenate & save
    final = pd.concat([viol_en, tree_en], ignore_index=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(args.out, index=False)

    print(f"Combined dataset saved: {args.out} ({len(final):,} rows)")

if __name__ == "__main__":
    main()