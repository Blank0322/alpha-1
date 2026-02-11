from __future__ import annotations

import pandas as pd

from .indicators import ema, rsi


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d['ema_fast'] = ema(d['close'], 12)
    d['ema_slow'] = ema(d['close'], 26)
    d['rsi14'] = rsi(d['close'], 14)

    d['long_entry'] = (d['ema_fast'] > d['ema_slow']) & (d['rsi14'] > 55)
    d['exit'] = (d['ema_fast'] < d['ema_slow']) | (d['rsi14'] < 45)
    return d
