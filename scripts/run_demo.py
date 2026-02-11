from __future__ import annotations

import math

import pandas as pd

from alpha1.strategy import generate_signals
from alpha1.backtest import run


def make_mock(n: int = 500) -> pd.DataFrame:
    px = 100.0
    out = []
    for i in range(n):
        px *= 1 + (0.0012 * math.sin(i / 15.0) + 0.0003)
        if i % 110 == 0 and i > 0:
            px *= 0.96
        out.append({'close': px})
    return pd.DataFrame(out)


def main() -> None:
    df = make_mock()
    sig = generate_signals(df)
    res = run(sig)
    print('alpha-1 demo result')
    print(f'- trades: {res.trades}')
    print(f'- total_return: {res.total_return:.2%}')
    print(f'- max_drawdown: {res.max_drawdown:.2%}')


if __name__ == '__main__':
    main()
