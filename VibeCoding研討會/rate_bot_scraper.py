#!/usr/bin/env python3
"""Scrape exchange rates from BOT and save to Excel.

Usage:
  python rate_bot_scraper.py -o rates.xlsx

Dependencies: requests, beautifulsoup4, pandas, openpyxl
"""
from __future__ import annotations
import argparse
from datetime import datetime
import sys

import requests
from bs4 import BeautifulSoup
import pandas as pd


def fetch_rates(url: str = "https://rate.bot.com.tw/xrt?Lang=zh-TW") -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0 (compatible)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")
    if table is None:
        raise RuntimeError("Could not find exchange rate table on the page")

    # Extract header names (cleaned)
    thead = table.find("thead")
    if thead:
        raw_headers = [th.get_text(separator=" ", strip=True) for th in thead.find_all("th")]
    else:
        raw_headers = []

    raw_headers = [h.replace("\n", " ").strip() for h in raw_headers]

    rows = []
    tbody = table.find("tbody")
    if not tbody:
        raise RuntimeError("No table body found")

    for tr in tbody.find_all("tr"):
        cols = [td.get_text(separator=" ", strip=True) for td in tr.find_all("td")]
        # Normalize whitespace inside each cell
        cols = [" ".join(c.split()) for c in cols]
        rows.append(cols)

    if not rows:
        return pd.DataFrame()

    max_cols = max(len(r) for r in rows)
    # Ensure header length matches
    if len(raw_headers) < max_cols:
        # Fill missing headers with generic names
        for i in range(len(raw_headers), max_cols):
            raw_headers.append(f"Col_{i+1}")
    raw_headers = raw_headers[:max_cols]

    # Normalize rows to max_cols
    norm_rows = [r + [""] * (max_cols - len(r)) if len(r) < max_cols else r[:max_cols] for r in rows]

    df = pd.DataFrame(norm_rows, columns=raw_headers)
    return df


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Scrape BOT exchange rates and save to Excel")
    parser.add_argument("-o", "--output", default="rates.xlsx", help="Output Excel file path")
    args = parser.parse_args(argv)

    try:
        df = fetch_rates()
    except Exception as e:
        print("Error fetching rates:", e, file=sys.stderr)
        return 2

    if df.empty:
        print("No data scraped.")
        return 1

    # Add timestamp column
    df["ScrapedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write to Excel
    try:
        df.to_excel(args.output, index=False, engine="openpyxl")
    except Exception as e:
        print("Error writing Excel file:", e, file=sys.stderr)
        return 3

    print(f"Wrote {len(df)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
