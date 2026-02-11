from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .backtest import run
from .strategy import generate_signals


@dataclass(frozen=True)
class WFWindow:
    train_start: int
    train_end: int
    test_start: int
    test_end: int


@dataclass(frozen=True)
class WFSummary:
    windows: int
    avg_return: float
    avg_drawdown: float
    total_trades: int


def make_windows(n: int, train_size: int = 200, test_size: int = 50, step: int = 50) -> list[WFWindow]:
    out: list[WFWindow] = []
    i = 0
    while i + train_size + test_size <= n:
        out.append(
            WFWindow(
                train_start=i,
                train_end=i + train_size,
                test_start=i + train_size,
                test_end=i + train_size + test_size,
            )
        )
        i += step
    return out


def run_walkforward(df: pd.DataFrame, train_size: int = 200, test_size: int = 50, step: int = 50) -> tuple[pd.DataFrame, WFSummary]:
    windows = make_windows(len(df), train_size=train_size, test_size=test_size, step=step)
    rows = []

    for idx, w in enumerate(windows, 1):
        # Strategy has fixed params for now; train slice reserved for future optimization
        _train = df.iloc[w.train_start:w.train_end].copy()
        test = df.iloc[w.test_start:w.test_end].copy()

        sig = generate_signals(test)
        res = run(sig)
        rows.append(
            {
                "window": idx,
                "train_range": f"[{w.train_start},{w.train_end})",
                "test_range": f"[{w.test_start},{w.test_end})",
                "trades": res.trades,
                "total_return": res.total_return,
                "max_drawdown": res.max_drawdown,
            }
        )

    detail = pd.DataFrame(rows)
    if detail.empty:
        summary = WFSummary(0, 0.0, 0.0, 0)
    else:
        summary = WFSummary(
            windows=int(detail.shape[0]),
            avg_return=float(detail["total_return"].mean()),
            avg_drawdown=float(detail["max_drawdown"].mean()),
            total_trades=int(detail["trades"].sum()),
        )
    return detail, summary
