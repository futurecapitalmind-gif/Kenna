# Kenna - AI Trading Telegram Bot Mentor

Kenna is a Telegram-first trading mentor that monitors live forex and gold market data, runs technical analysis, and helps traders interpret risk and opportunity with clear, actionable insights.

## What it does

- Analyzes live market data for major forex pairs and gold
- Uses technical indicators such as RSI, MACD, and moving averages
- Generates simple bullish/bearish/neutral trading signals
- Provides mentor-style guidance and risk awareness
- Runs inside Telegram so you can check market conditions from chat

## Supported instruments

- EURUSD
- USDJPY
- GBPUSD
- AUDUSD
- XAUUSD / GOLD

## Tech stack

- Python 3.11+
- python-telegram-bot
- yfinance
- pandas / numpy
- python-dotenv

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Commands

```text
/start
/help
/analyze EURUSD
/gold
/signals
/price EURUSD
```

## Risk disclaimer

This bot is for educational and informational use only. It does not provide financial advice and should not be relied upon as a trading recommendation.
