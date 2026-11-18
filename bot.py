import asyncio, os, requests, pytz
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = set()

def get_namoz():
    try:
        r = requests.get("https://api.aladhan.com/v1/timingsByCity?city=Idlib&country=Syria&method=5", timeout=10)
        t = r.json()['data']['timings']
        return f"🕌 Idlib - Bugungi Namoz Vaqtlari\n\n🌅 Bomdod: {t['Fajr']}\n☀️ Quyosh: {t['Sunrise']}\n🕌 Peshin: {t['Dhuhr']}\n🕌 Asr: {t['Asr']}\n🌇 Shom: {t['Maghrib']}\n🌙 Xufton: {t['Isha']}"
    except:
        return "Hozir vaqtlarni olib bo'lmadi."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CHAT_IDS.add(update.effective_chat.id)
    await update.message.reply_text(get_namoz() + "\n\n✅ Har kuni 8:00 da keladi.")

async def send_daily(context: ContextTypes.DEFAULT_TYPE):
    for cid in list(CHAT_IDS):
        try:
            await context.bot.send_message(cid, get_namoz())
        except:
            pass

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    tz = pytz.timezone("Asia/Damascus")
    await app.initialize()
    if app.job_queue:
        app.job_queue.run_daily(send_daily, time=time(hour=5, minute=0, tzinfo=tz))
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
