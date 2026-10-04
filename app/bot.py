from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def rsi(series: pd.Series, period: int = 14) -> float:
    if len(series) < period + 1:
        return 50.0
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean().iloc[-1]
    avg_loss = loss.rolling(window=period, min_periods=period).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[float, float, float]:
    if len(series) < slow + signal:
        return 0.0, 0.0, 0.0
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return round(float(macd_line.iloc[-1]), 5), round(float(signal_line.iloc[-1]), 5), round(float(histogram.iloc[-1]), 5)


def sma(series: pd.Series, window: int) -> float:
    if len(series) < window:
        return float(series.iloc[-1])
    return round(float(series.rolling(window=window).mean().iloc[-1]), 5)


def support_resistance(series: pd.Series, lookback: int = 20) -> Tuple[float, float]:
    recent = series.tail(lookback)
    support = float(recent.min())
    resistance = float(recent.max())
    return support, resistance


def generate_signal(symbol: str, history: pd.DataFrame) -> Dict[str, object]:
    history = history.copy().dropna(subset=["Close", "High", "Low"])
    if history.empty:
        return {
            "symbol": symbol.upper(),
            "signal": "HOLD",
            "confidence": 0.0,
            "mentor_note": "No valid market history was returned.",
        }

    closes = history["Close"].astype(float)
    highs = history["High"].astype(float)
    lows = history["Low"].astype(float)

    current_price = float(closes.iloc[-1])
    previous_close = float(closes.iloc[-2]) if len(closes) > 1 else current_price
    change_pct = ((current_price - previous_close) / previous_close * 100) if previous_close else 0.0

    rsi_value = rsi(closes, 14)
    macd_value, signal_value, histogram = macd(closes, 12, 26, 9)
    sma_short = sma(closes, 20)
    sma_long = sma(closes, 50)
    support, resistance = support_resistance(lows), support_resistance(highs)[1]
    # support_resistance should be computed on low/high separately; this line fixes tuple handling
    support_low, _ = support_resistance(lows)
    _, resistance_high = support_resistance(highs)
    support = support_low
    resistance = resistance_high

    score = 50.0
    if rsi_value < 30:
        score += 20
    elif rsi_value > 70:
        score -= 20

    if macd_value > signal_value:
        score += 15
    else:
        score -= 15

    if sma_short > sma_long:
        score += 15
    else:
        score -= 15

    if change_pct > 0:
        score += 8
    else:
        score -= 8

    if score >= 60:
        signal = "BUY"
    elif score <= 40:
        signal = "SELL"
    else:
        signal = "HOLD"

    confidence = min(max(abs(score - 50) / 50, 0.55), 0.95)
    trend = "Bullish" if sma_short > sma_long else "Bearish"

    if signal == "BUY":
        mentor_note = (
            "Momentum is constructive. Watch for continuation above support, and keep risk disciplined with a clear stop."
        )
    elif signal == "SELL":
        mentor_note = (
            "Momentum is weak. Prefer confirmation below support and avoid forced entries while the trend remains fragile."
        )
    else:
        mentor_note = (
            "The market is balanced. Wait for a cleaner breakout or rejection near key levels before committing capital."
        )

    return {
        "symbol": symbol.upper(),
        "signal": signal,
        "confidence": round(confidence, 3),
        "trend": trend,
        "current_price": round(current_price, 5),
        "change_pct": round(change_pct, 4),
        "rsi": rsi_value,
        "macd": macd_value,
        "signal_line": signal_value,
        "histogram": histogram,
        "sma_short": sma_short,
        "sma_long": sma_long,
        "support": round(float(support), 5),
        "resistance": round(float(resistance), 5),
        "mentor_note": mentor_note,
    }


def format_signal_message(signal_data: Dict[str, object]) -> str:
    return (
        f"📊 {signal_data['symbol']}\n"
        f"Bias: {signal_data['signal']} | Confidence: {signal_data['confidence']:.0%}\n"
        f"Price: {signal_data['current_price']} | Change: {signal_data['change_pct']:+.2f}%\n"
        f"Trend: {signal_data['trend']}\n"
        f"RSI: {signal_data['rsi']} | MACD: {signal_data['macd']}\n"
        f"SMA 20: {signal_data['sma_short']} | SMA 50: {signal_data['sma_long']}\n"
        f"Support: {signal_data['support']} | Resistance: {signal_data['resistance']}\n"
        f"Mentor: {signal_data['mentor_note']}"
    )
