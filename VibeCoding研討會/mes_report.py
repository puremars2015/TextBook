#!/usr/bin/env python3
"""Fetch today's production from MES and export to Excel.

Usage:
  python mes_report.py output.xlsx --config mes_api_config.json

Config (JSON) example provided in `mes_api_config.json`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import requests


def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_today_production(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    base = config.get("base_url")
    endpoint = config.get("endpoint", "/api/production/today")
    url = base.rstrip("/") + endpoint
    headers = {}
    token = config.get("token")
    if token:
        headers[config.get("auth_header", "Authorization")] = token

    params = config.get("params", {})

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Expecting either a list at top-level or an object with a list under a key
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # try common keys
        for k in ("data", "items", "results"):
            if k in data and isinstance(data[k], list):
                return data[k]
    raise ValueError("Unexpected response format from MES API")


def map_records(records: List[Dict[str, Any]], mapping: Dict[str, str]) -> List[Dict[str, Any]]:
    out = []
    for r in records:
        out.append({
            "工單名稱": r.get(mapping.get("work_order"), ""),
            "產出重量": r.get(mapping.get("weight"), ""),
            "產品名稱": r.get(mapping.get("product"), ""),
        })
    return out


def write_excel(rows: List[Dict[str, Any]], path: Path) -> None:
    df = pd.DataFrame(rows, columns=["工單名稱", "產出重量", "產品名稱"])
    df.to_excel(path, index=False)


def main(argv: List[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="Export today's MES production to Excel")
    p.add_argument("output", help="Output Excel file path (xlsx)")
    p.add_argument("--config", default="mes_api_config.json", help="Path to JSON config file")
    args = p.parse_args(argv)

    out_path = Path(args.output)
    cfg_path = Path(args.config)

    try:
        cfg = load_config(cfg_path)
    except Exception as e:
        print(f"Failed to load config: {e}")
        return 2

    try:
        records = fetch_today_production(cfg)
    except Exception as e:
        print(f"Failed to fetch production data: {e}")
        return 3

    mapping = cfg.get("field_map", {"work_order": "work_order", "weight": "weight", "product": "product_name"})
    rows = map_records(records, mapping)

    try:
        write_excel(rows, out_path)
    except Exception as e:
        print(f"Failed to write Excel: {e}")
        return 4

    print(f"Wrote {len(rows)} rows to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
