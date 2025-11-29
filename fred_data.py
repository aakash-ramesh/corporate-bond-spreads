#!/usr/bin/env python3
"""
Fetch full-history time series from FRED and save as a single wide CSV.

Usage:
  # 1) Install deps
  #    pip install pandas fredapi pyarrow  # pyarrow optional (for Parquet)
  #
  # 2A) Provide API key via env:
  #    export FRED_API_KEY="YOUR_KEY"
  #    python fetch_fred_series.py
  #
  # 2B) Or pass via flag:
  #    python fetch_fred_series.py --api-key YOUR_KEY --out fred_data.csv --parquet fred_data.parquet
"""

from __future__ import annotations
import os
import sys
import time
import argparse
from typing import Dict, List
import pandas as pd
import fredapi
from fredapi import Fred

SERIES: Dict[str, str] = {
    # ID : Friendly name
    "BAMLC0A0CMEY": "ICE BofA US Corporate Index Effective Yield",
    "BAMLH0A0HYM2EY": "ICE BofA US High Yield Index Effective Yield",
    "BAMLC0A0CM": "ICE BofA US Corporate Index OAS",
    "BAMLH0A0HYM2": "ICE BofA US High Yield Index OAS",
    "VIXCLS": "CBOE Volatility Index (VIX)",
    "DGS10": "Market Yield on U.S. Treasury (10Y CMT)",
    "DGS5": "Market Yield on U.S. Treasury (5Y CMT)",
    "DGS2": "Market Yield on U.S. Treasury (2Y CMT)",
    "DGS30": "Market Yield on U.S. Treasury (30Y CMT)",
    "CPIAUCSL": "CPI: All Items",
    "CPILFESL": "CPI: All Items less Food & Energy",
    "UNRATE": "Unemployment Rate",
    "CCSA": "Continued Claims (Insured Unemployment)",
}

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Download FRED time series into a wide CSV/Parquet.")
    p.add_argument("--api-key", default=os.getenv("FRED_API_KEY"), help="FRED API key (or set FRED_API_KEY).")
    p.add_argument("--out", default="fred_series_all.csv", help="Output CSV filename.")
    p.add_argument("--parquet", default=None, help="Optional Parquet filename to also write.")
    p.add_argument("--timeout", type=float, default=0.0, help="Sleep seconds between requests (avoid rate limits).")
    return p.parse_args()

def fetch_all(fred: Fred, series_ids: List[str]) -> pd.DataFrame:
    frames = []
    for i, sid in enumerate(series_ids, 1):
        # Get full history for each series as a pandas.Series indexed by datetime
        s = fred.get_series(sid)
        s.index = pd.to_datetime(s.index)  # ensure datetime index
        s.name = sid
        frames.append(s)
        # Optional pause for rate limiting
        if args.timeout > 0 and i < len(series_ids):
            time.sleep(args.timeout)
    # Outer-join on the union of all dates (different series have different frequencies)
    df = pd.concat(frames, axis=1, join="outer").sort_index()
    return df

def add_metadata_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add friendly column names and keep IDs."""
    # Keep original ID columns; also add a multiindex header with Friendly Name
    friendly = {sid: SERIES[sid] for sid in df.columns if sid in SERIES}
    df_friendly = df.rename(columns=friendly)
    # Build a two-level column MultiIndex: (ID, Friendly Name)
    cols = pd.MultiIndex.from_tuples([(sid, SERIES.get(sid, sid)) for sid in df.columns],
                                     names=["FRED_ID", "Description"])
    df.columns = cols
    # Put a flat friendly copy too (optional): comment out if you only want MultiIndex
    df_out = df.copy()
    # Also attach a flat friendly-only view as a second file if desired.
    return df_out, df_friendly

if __name__ == "__main__":
    args = parse_args()
    if not args.api_key:
        sys.stderr.write(
            "Error: FRED API key not provided. Use --api-key or set FRED_API_KEY env var.\n"
        )
        sys.exit(1)

    fred = Fred(api_key=args.api_key)

    series_ids = list(SERIES.keys())
    df = fetch_all(fred, series_ids)

    # Attach both MultiIndex (ID, Name) and a flat friendly column set for convenience
    df_multi, df_friendly = add_metadata_columns(df)

    # Write CSV (MultiIndex columns are preserved; some tools flatten them—Excel will show two header rows)
    df_multi.to_csv(args.out, index_label="Date")
    print(f"Wrote CSV: {args.out}  (columns are a MultiIndex: FRED_ID, Description)")

    if args.parquet:
        try:
            df_multi.to_parquet(args.parquet, engine="pyarrow")
            print(f"Wrote Parquet: {args.parquet}")
        except Exception as e:
            sys.stderr.write(f"Parquet write failed (install pyarrow?): {e}\n")

    # Also write a helper CSV with flat friendly names (no MultiIndex), if you want:
    friendly_out = args.out.replace(".csv", "_friendly.csv")
    df_friendly.to_csv(friendly_out, index_label="Date")
    print(f"Wrote CSV with friendly column names: {friendly_out}")
