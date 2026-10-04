# Kenna - AI Trading Telegram Bot Mentor

Kenna is a Telegram bot that provides live market insight for forex and gold using technical analysis and mentor-style commentary. It is designed to help traders monitor instruments, check momentum, and understand bias without having to stare at charts all day.

## Features

- Live forex and gold market analysis
- RSI, MACD, moving-average, support and resistance checks
- Trade signal generation with confidence scoring
- Mentor-style suggestions and risk awareness
- Telegram commands for quick market checks
- YAML/JSON-ready configuration via environment variables

## Supported pairs

- EURUSD
- USDJPY
- GBPUSD
- AUDUSD
- XAUUSD / GOLD

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Environment variables

```env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_ADMIN_ID=your_telegram_id
MARKET_DATA_PROVIDER=yahoo
DEFAULT_TIMEFRAME=1h
MIN_SIGNAL_CONFIDENCE=0.65
```

## Commands

```text
/start
/help
/analyze EURUSD
/analyze XAUUSD
/gold
/signals
/price EURUSD
```
