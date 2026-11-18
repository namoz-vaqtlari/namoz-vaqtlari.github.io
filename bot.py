import asyncio, os, requests, pytz
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        def log_message(self, *a):
            pass
    threading.Thread(target=HTTPServer(("0.0.0.0", port), H).serve_forever, daemon=True).start()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = set()

def get_namoz():
    try:
        r = requests.get("https://api.aladhan.com/v1/timingsByCity?city=Idlib&country=Syria&method=5", timeout=10)
        t = r.json()['data']['timings']
        return f"🕌 Idlib - Bugungi Namoz Vaqtlari:\n\nBomdod: {t['Fajr']}\nQuyosh: {t['Sunrise']}\nPeshin: {t['Dhuhr']}\nAsr: {t['Asr']}\nShom: {t['Maghrib']}\nXufton: {t['Isha']}"
    except:
        return "Hozir vaqtlarni olib bo'lmadi, birozdan keyin urinib ko'ring."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CHAT_IDS.add(update.effective_chat.id)
    await update.message.reply_text(get_namoz())

async def send_daily(context: ContextTypes.DEFAULT_TYPE):
    for cid in list(CHAT_IDS):
        try:
            await context.bot.send_message(chat_id=cid, text=get_namoz())
        except:
            pass

async def main():
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    tz = pytz.timezone("Asia/Damascus")
    if app.job_queue:
        app.job_queue.run_daily(send_daily, time=time(hour=0, minute=5, tzinfo=tz))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
