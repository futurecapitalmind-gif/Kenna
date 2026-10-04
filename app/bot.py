from __future__ import annotations

from typing import List

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app.analysis import format_signal_message, generate_signal
from app.config import settings
from app.market_data import get_major_pairs, get_market_snapshot


def _normalize_symbol(args: List[str], fallback: str = "EURUSD") -> str:
    if args:
        raw = args[0].upper()
        if raw in {"GOLD", "XAUUSD"}:
            return "XAUUSD"
        return raw
    return fallback


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "👋 Welcome to Kenna, your AI trading mentor.\n\n"
        "Use these commands:\n"
        "/analyze EURUSD\n"
        "/gold\n"
        "/signals\n"
        "/price EURUSD\n"
        "/help\n\n"
        "I scan forex and gold markets, highlight trend bias, and keep the guidance simple and disciplined."
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "/start - open the trading mentor\n"
        "/analyze <symbol> - full technical breakdown\n"
        "/gold - gold analysis\n"
        "/signals - snapshot of major pairs\n"
        "/price <symbol> - quick price check\n"
        "/help - this menu"
    )
    await update.message.reply_text(text)


async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    symbol = _normalize_symbol(context.args, "EURUSD")
    try:
        snapshot = get_market_snapshot(symbol, period="5d", interval="1h")
        signal = generate_signal(symbol, snapshot["history"])
        message = (
            f"📈 {symbol} Market Analysis\n"
            f"Current Price: {snapshot['price']}\n"
            f"1H Change: {snapshot['change_pct']:+.2f}%\n"
            f"High: {snapshot['high']} | Low: {snapshot['low']}\n"
            f"Signal: {signal['signal']} | Confidence: {signal['confidence']:.0%}\n"
            f"Trend: {signal['trend']}\n"
            f"RSI: {signal['rsi']} | SMA 20: {signal['sma_short']} | SMA 50: {signal['sma_long']}\n"
            f"Mentor: {signal['mentor_note']}"
        )
        await update.message.reply_text(message)
    except Exception as exc:
        await update.message.reply_text(f"⚠️ I could not analyze {symbol}. Error: {exc}")


async def gold_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    symbol = "XAUUSD"
    try:
        snapshot = get_market_snapshot(symbol, period="5d", interval="1h")
        signal = generate_signal(symbol, snapshot["history"])
        await update.message.reply_text(format_signal_message(signal))
    except Exception as exc:
        await update.message.reply_text(f"⚠️ Gold analysis unavailable: {exc}")


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    symbol = _normalize_symbol(context.args, "EURUSD")
    try:
        snapshot = get_market_snapshot(symbol, period="1d", interval="15m")
        text = (
            f"💵 {symbol}\n"
            f"Price: {snapshot['price']}\n"
            f"Change: {snapshot['change_pct']:+.2f}%\n"
            f"Open: {snapshot['open']}\n"
            f"High: {snapshot['high']}\n"
            f"Low: {snapshot['low']}\n"
            f"Volume: {snapshot['volume']}"
        )
        await update.message.reply_text(text)
    except Exception as exc:
        await update.message.reply_text(f"⚠️ Price check failed for {symbol}: {exc}")


async def signals_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = []
    for symbol in get_major_pairs():
        try:
            snapshot = get_market_snapshot(symbol, period="2d", interval="1h")
            signal = generate_signal(symbol, snapshot["history"])
            lines.append(f"{symbol}: {signal['signal']} ({signal['confidence']:.0%})")
        except Exception:
            lines.append(f"{symbol}: unavailable")
    await update.message.reply_text("📉 Signal Snapshot\n" + "\n".join(lines))


def build_application() -> Application:
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Add it to your .env file.")

    application = Application.builder().token(settings.telegram_bot_token).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analyze", analyze_command))
    application.add_handler(CommandHandler("gold", gold_command))
    application.add_handler(CommandHandler("price", price_command))
    application.add_handler(CommandHandler("signals", signals_command))
    return application


def run_bot() -> None:
    app = build_application()
    print("Kenna bot is starting...")
    app.run_polling(allowed_updates=["message", "callback_query"])
