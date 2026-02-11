from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from alpha1.walkforward import run_walkforward
from scripts.run_demo import make_mock


def load_data(csv_path: str | None) -> pd.DataFrame:
    if not csv_path:
        return make_mock()
    df = pd.read_csv(csv_path)
    if "close" not in df.columns:
        raise ValueError("CSV must contain a 'close' column")
    return df[["close"]].dropna().reset_index(drop=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--csv")
    p.add_argument("--train", type=int, default=200)
    p.add_argument("--test", type=int, default=50)
    p.add_argument("--step", type=int, default=50)
    p.add_argument("--out", default="output/walkforward_summary.csv")
    args = p.parse_args()

    df = load_data(args.csv)
    detail, summary = run_walkforward(df, train_size=args.train, test_size=args.test, step=args.step)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    detail.to_csv(args.out, index=False)

    print("walk-forward summary")
    print(f"- windows: {summary.windows}")
    print(f"- total_trades: {summary.total_trades}")
    print(f"- avg_return: {summary.avg_return:.2%}")
    print(f"- avg_drawdown: {summary.avg_drawdown:.2%}")
    print(f"- detail_csv: {args.out}")


if __name__ == "__main__":
    main()
