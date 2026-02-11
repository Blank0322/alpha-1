from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Result:
    trades: int
    total_return: float
    max_drawdown: float


def run(df: pd.DataFrame, fee_bps: float = 6.0) -> Result:
    d = df.copy().reset_index(drop=True)
    pos = 0
    equity = [1.0]
    trades = 0
    fee = fee_bps / 10000

    for i in range(1, len(d)):
        if pos == 0 and bool(d.loc[i - 1, 'long_entry']):
            pos = 1
            trades += 1
            equity.append(equity[-1] * (1 - fee))
            continue

        if pos == 1 and bool(d.loc[i - 1, 'exit']):
            pos = 0
            equity.append(equity[-1] * (1 - fee))
            continue

        ret = d.loc[i, 'close'] / d.loc[i - 1, 'close'] - 1
        equity.append(equity[-1] * (1 + pos * ret))

    eq = pd.Series(equity)
    peak = eq.cummax()
    dd = (eq / peak - 1).min()
    return Result(trades=trades, total_return=float(eq.iloc[-1] - 1), max_drawdown=float(dd))
