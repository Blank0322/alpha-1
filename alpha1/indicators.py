from __future__ import annotations

import pandas as pd


def ema(s: pd.Series, span: int) -> pd.Series:
    return s.ewm(span=span, adjust=False).mean()


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    rs = up.ewm(alpha=1 / period, adjust=False).mean() / down.ewm(alpha=1 / period, adjust=False).mean()
    return 100 - (100 / (1 + rs))
