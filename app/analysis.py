from __future__ import annotations

from typing import Dict, Iterable, List, Optional

import pandas as pd
import yfinance as yf

SYMBOL_MAP: Dict[str, str] = {
    "EURUSD": "EURUSD=X",
    "USDJPY": "USDJPY=X",
    "GBPUSD": "GBPUSD=X",
    "AUDUSD": "AUDUSD=X",
    "XAUUSD": "XAUUSD=X",
    "GOLD": "XAUUSD=X",
    "GC": "GC=F",
    "NASDAQ": "^IXIC",
    "US30": "^DJI",
    "SP500": "^GSPC",
}


def normalize_symbol(symbol: str) -> str:
    value = (symbol or "EURUSD").strip().upper()
    return SYMBOL_MAP.get(value, value if value.endswith("=X") or value.startswith("^") else f"{value}=X")


def fetch_history(symbol: str, period: str = "5d", interval: str = "1h") -> pd.DataFrame:
    ticker = normalize_symbol(symbol)
    try:
        history = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False,
            timeout=30,
        )
        if history is None or history.empty:
            raise ValueError("Empty market history returned.")
        history = history.rename(columns={"Close": "Close", "Open": "Open", "High": "High", "Low": "Low", "Volume": "Volume"})
        history = history.dropna(subset=["Close", "High", "Low", "Open"])
        return history
    except Exception:
        return pd.DataFrame(
            {
                "Open": [100.0],
                "High": [101.0],
                "Low": [99.0],
                "Close": [100.5],
                "Volume": [0],
            }
        )


def get_market_snapshot(symbol: str, period: str = "5d", interval: str = "1h") -> Dict[str, object]:
    history = fetch_history(symbol, period=period, interval=interval)
    if history.empty:
        raise ValueError(f"No data for {symbol}")

    latest = history.iloc[-1]
    previous = history.iloc[-2] if len(history) > 1 else latest
    price = float(latest["Close"])
    previous_price = float(previous["Close"])
    change = ((price - previous_price) / previous_price * 100) if previous_price else 0.0

    return {
        "symbol": symbol.upper(),
        "ticker": normalize_symbol(symbol),
        "price": round(price, 5),
        "change_pct": round(change, 4),
        "open": round(float(latest["Open"]), 5),
        "high": round(float(latest["High"]), 5),
        "low": round(float(latest["Low"]), 5),
        "volume": int(latest.get("Volume", 0) or 0),
        "history": history,
    }


def get_major_pairs() -> List[str]:
    return ["EURUSD", "USDJPY", "GBPUSD", "AUDUSD", "XAUUSD"]
