# Kenna - AI Trading Telegram Bot Mentor

Kenna is a Telegram-first trading mentor that monitors live forex and gold market data, runs technical analysis, and helps traders interpret risk and opportunity with clear, actionable insights.

## What it does

- Analyzes live market data for major forex pairs and gold
- Uses technical indicators such as RSI, MACD, and moving averages
- Generates simple bullish/bearish/neutral trading signals
- Gives mentor-style guidance to help traders stay disciplined
- Runs inside Telegram so you can check market conditions from chat

## Supported instruments

- EURUSD
- USDJPY
- GBPUSD
- XAUUSD / GOLD
- AUDUSD
- NASDAQ (optional)

## Stack

- Python 3.11+
- FastAPI (optional lightweight API layer)
- python-telegram-bot
- pandas / numpy / scipy
- yfinance for live market data
- Telegram bot commands for analysis and signals

## Project layout

```text
Kenna/
├── app/
│   ├── __init__.py
│   ├── analysis.py
│   ├── bot.py
│   ├── config.py
│   └── market_data.py
├── tests/
│   └── test_analysis.py
├── .env.example
├── Dockerfile
├── README.md
├── docker-compose.yml
├── main.py
├── requirements.txt
└── .gitignore
```

## Quick start

### 1) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure Telegram token

```bash
cp .env.example .env
```

Then update `.env` with a valid Telegram bot token:

```env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_ADMIN_ID=your_telegram_user_id
```

### 4) Run the bot

```bash
python main.py
```

## Telegram commands

```text
/start            Show onboarding and commands
/help             Display help
/analyze EURUSD   Analyze a forex pair
/gold             Analyze gold (XAUUSD)
/signals          Show signal snapshot for major pairs
/price EURUSD     Show the current price snapshot
```

## Market data source

This starter uses Yahoo Finance for live market pricing and historical candles. It is ideal for a development and trading-mentor environment without a paid broker or data provider.

## Risk disclaimer

This bot is for educational and informational use only. It does not provide financial advice, and it is not a guarantee of profitable trades. Always confirm signals with your own research and sound risk management.

## Roadmap

- Add trade journal and portfolio tracking
- Add multi-timeframe analysis
- Add signal persistence to PostgreSQL
- Add premium signal providers and news sentiment feeds
- Add backtesting engine
- Add user profile and alert preferences
