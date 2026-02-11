from __future__ import annotations

import argparse
import math
import os
import sys

import pandas as pd

# allow running as: python scripts/run_demo.py
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from alpha1.backtest import run
from alpha1.strategy import generate_signals


def make_mock(n: int = 500) -> pd.DataFrame:
    px = 100.0
    out = []
    for i in range(n):
        px *= 1 + (0.0012 * math.sin(i / 15.0) + 0.0003)
        if i % 110 == 0 and i > 0:
            px *= 0.96
        out.append({"close": px})
    return pd.DataFrame(out)


def load_data(csv_path: str | None) -> pd.DataFrame:
    if not csv_path:
        return make_mock()
    df = pd.read_csv(csv_path)
    if "close" not in df.columns:
        raise ValueError("CSV must contain a 'close' column")
    return df[["close"]].dropna().reset_index(drop=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", help="Optional CSV path with column: close")
    args = p.parse_args()

    df = load_data(args.csv)
    sig = generate_signals(df)
    res = run(sig)
    print("alpha-1 demo result")
    print(f"- trades: {res.trades}")
    print(f"- total_return: {res.total_return:.2%}")
    print(f"- max_drawdown: {res.max_drawdown:.2%}")


if __name__ == "__main__":
    main()
