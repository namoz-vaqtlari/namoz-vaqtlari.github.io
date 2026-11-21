import os
import requests
from datetime import datetime
import pytz
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Fu'ah / Idlib - Suriya
CITY = "Idlib"
COUNTRY = "Syria"

def get_prayer_times():
    try:
        url = f"https://api.aladhan.com/v1/timingsByCity?city={CITY}&country={COUNTRY}&method=5"
        r = requests.get(url, timeout=10)
        data = r.json()["data"]["timings"]
        return data
    except:
        return None

def prayer_text():
    t = get_prayer_times()
    if not t:
        return "Hozir namoz vaqtlarini olib bo'lmadi. Keyinroq urinib ko'ring."
    tz = pytz.timezone("Asia/Damascus")
    today = datetime.now(tz).strftime("%d.%m.%Y")
    return (
        f"🕋 *Namoz vaqtlari - Fu'ah / Idlib*\n"
        f"📅 {today}\n\n"
        f"🌅 Bomdod: {t['Fajr']}\n"
        f"🌞 Quyosh: {t['Sunrise']}\n"
        f"☀️ Peshin: {t['Dhuhr']}\n"
        f"🌤️ Asr: {t['Asr']}\n"
        f"🌇 Shom: {t['Maghrib']}\n"
        f"🌙 Xufton: {t['Isha']}\n\n"
        f"🤲 Alloh ibodatlaringni qabul qilsin!"
    )

MORNING = """🌅 *ERTALABKI ZIKRLAR*

1. *Oyatal Kursiy*
Allohu la ilaha illa Huwal Hayyul Qoyyum...

2. *Ixlos, Falaq, Nos* - 3 martadan

3. *Subhanallohi va bihamdihi* - 100 marta

4. *La ilaha illallohu vahdahu la sharika lah, lahul mulku va lahul hamdu va Huva 'ala kulli shay'in Qodir* - 100 marta

5. *Astag'firulloh* - 100 marta

6. *Allohumma bika asbahnna va bika amsayna va bika nahya va bika namutu va ilaykan nushur*

7. *Hasbiyallohu la ilaha illa Huva, 'alayhi tavakkaltu va Huva Robbul 'arshil 'azim* - 7 marta

🤲 Ertalabingiz muborak bo'lsin!
"""

EVENING = """🌙 *KECHKI ZIKRLAR*

1. *Oyatal Kursiy*
Allohu la ilaha illa Huwal Hayyul Qoyyum...

2. *Ixlos, Falaq, Nos* - 3 martadan

3. *Subhanallohi va bihamdihi* - 100 marta

4. *La ilaha illallohu vahdahu la sharika lah, lahul mulku va lahul hamdu va Huva 'ala kulli shay'in Qodir* - 100 marta

5. *Astag'firulloh* - 100 marta

6. *Allohumma bika amsayna va bika asbahnna va bika nahya va bika namutu va ilaykal masiyr*

7. *Hasbiyallohu la ilaha illa Huva, 'alayhi tavakkaltu va Huva Robbul 'arshil 'azim* - 7 marta

8. *A'uzu bikalimatillahit tammati min sharri ma xolaq* - 3 marta

🤲 Kechangiz xayrli bo'lsin!
"""

KEYBOARD = ReplyKeyboardMarkup(
    [["🕋 Namoz vaqtlari"], ["🌅 Ertalabki zikrlar", "🌙 Kechki zikrlar"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! 🤲\nFu'ah / Idlib namoz vaqtlari botiga xush kelibsiz.\n\nPastdagi tugmalardan birini tanlang:",
        reply_markup=KEYBOARD
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🕋 Namoz vaqtlari":
        await update.message.reply_text(prayer_text(), parse_mode="Markdown")
    elif text == "🌅 Ertalabki zikrlar":
        await update.message.reply_text(MORNING, parse_mode="Markdown")
    elif text == "🌙 Kechki zikrlar":
        await update.message.reply_text(EVENING, parse_mode="Markdown")
    else:
        await update.message.reply_text("Pastdagi tugmalardan birini tanlang 👇", reply_markup=KEYBOARD)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
