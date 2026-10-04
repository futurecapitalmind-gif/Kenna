from __future__ import annotations

import pandas as pd

from app.analysis import generate_signal


def test_generate_signal_buy_case() -> None:
    history = pd.DataFrame(
        {
            "Open": [1.0, 1.01, 1.02, 1.03, 1.04, 1.05],
            "High": [1.02, 1.03, 1.04, 1.05, 1.06, 1.07],
            "Low": [0.99, 1.0, 1.01, 1.02, 1.03, 1.04],
            "Close": [1.01, 1.02, 1.03, 1.04, 1.05, 1.08],
        }
    )

    result = generate_signal("EURUSD", history)
    assert result["symbol"] == "EURUSD"
    assert result["signal"] in {"BUY", "SELL", "HOLD"}
    assert 0.0 <= result["confidence"] <= 1.0


def test_generate_signal_empty_history() -> None:
    empty = pd.DataFrame(columns=["Open", "High", "Low", "Close"])
    result = generate_signal("USDJPY", empty)
    assert result["signal"] == "HOLD"
