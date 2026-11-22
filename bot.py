import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

def get_keyboard():
    return ReplyKeyboardMarkup([["Namoz vaqtlari"]], resize_keyboard=True)

def get_prayer_times():
    try:
        url = "https://api.aladhan.com/v1/timingsByCity?city=Idlib&country=Syria&method=13"
        r = requests.get(url, timeout=10).json()
        t = r["data"]["timings"]
        hijri = r["data"]["date"]["hijri"]
        return (
            f"Namoz vaqtlari - Idlib\n"
            f"Hijriy: {hijri['day']} {hijri['month']['en']} {hijri['year']}\n\n"
            f"Bomdod: {t['Fajr']}\n"
            f"Quyosh: {t['Sunrise']}\n"
            f"Peshin: {t['Dhuhr']}\n"
            f"Asr: {t['Asr']}\n"
            f"Shom: {t['Maghrib']}\n"
            f"Xufton: {t['Isha']}"
        )
    except Exception as e:
        return f"Xatolik: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Tugmani bosing:", reply_markup=get_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Namoz vaqtlari":
        await update.message.reply_text(get_prayer_times(), reply_markup=get_keyboard())
    else:
        await update.message.reply_text("Tugmani bosing:", reply_markup=get_keyboard())

def main():
    port = int(os.environ.get("PORT", 10000))
    def run_server():
        HTTPServer(("0.0.0.0", port), BaseHTTPRequestHandler).serve_forever()
    threading.Thread(target=run_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
