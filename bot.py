import asyncio, os, requests, pytz
from datetime import datetime, time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = None
CITY = "Idlib"
COUNTRY = "Syria"
TZ = pytz.timezone("Asia/Damascus")

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        def log_message(self, *a):
            pass
    threading.Thread(target=HTTPServer(('0.0.0.0', port), H).serve_forever, daemon=True).start()

KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🕋 Namoz vaqtlari")],
        [KeyboardButton("🌅 Ertalabki zikrlar"), KeyboardButton("🌙 Kechki zikrlar")],
    ],
    resize_keyboard=True
)

ERTALABKI_ZIKR = """🌅 ERTALABKI ZIKRLAR - IDLIB

1. Oyatul Kursiy - 1 marta
اللَّهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ...
Ma'nosi: Allohdan o'zga iloh yo'q, U tirik va bardavomdir.

2. Ixlos, Falaq, Nos - har biri 3 martadan
Ixlos: قُلْ هُوَ اللَّهُ أَحَدٌ...
Falaq: قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ...
Nos: قُلْ أَعُوذُ بِرَبِّ النَّاسِ...

3. Asbahna va asbahal mulku lillah - 1 marta
أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ...
Ma'nosi: Tongga kirdik, mulk ham Allohniki bo'lib tongga kirdi.

4. Allohumma bika asbahna - 1 marta
اللَّهُمَّ بِكَ أَصْبَحْنَا...
Ma'nosi: Allohim, Sening yordaming bilan tongga kirdik.

5. Sayyidul istig'for - 1 marta
اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ...
Ma'nosi: Allohim, Sen mening Robbimsan...

6. Allohumma inni asbahtu ushhiduka - 4 marta
اللَّهُمَّ إِنِّي أَصْبَحْتُ أُشْهِدُكَ...
Ma'nosi: Allohim, men tongga kirdim, Seni guvoh qilaman...

7. Allohumma ma asbaha bi - 1 marta
اللَّهُمَّ مَا أَصْبَحَ بِي مِنْ نِعْمَةٍ...
Ma'nosi: Menga yetgan har qanday ne'mat faqat Sendan.

8. Allohumma 'afini - 3 marta
اللَّهُمَّ عَافِنِي فِي بَدَنِي...
Ma'nosi: Allohim, badanimda menga ofiyat ber.

9. Allohumma inni a'uzu bika - 3 marta
اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْكُفْرِ...
Ma'nosi: Allohim, kufrdan, kambag'allikdan Senga panoh tilayman.

10. Hasbiyallohu - 7 marta
حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ...
Ma'nosi: Alloh menga kifoya.

11. Bismillahilladhiy - 3 marta
بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ...
Ma'nosi: Allohning nomi bilan...

12. Roziytu billahi - 3 marta
رَضِيتُ بِاللَّهِ رَبًّا...
Ma'nosi: Allohni Robb deb rozi bo'ldim.

13. Ya Hayyu ya Qayyum - 1 marta
يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ...
Ma'nosi: Ey tirik, ey bardavom Zot!

14. Asbahna 'ala fitratil Islam - 1 marta
أَصْبَحْنَا عَلَى فِطْرَةِ الْإِسْلَامِ...
Ma'nosi: Islom fitratida tongga kirdik.

15. Subhanalloh va bihamdih - 100 marta
سُبْحَانَ اللَّهِ وَبِحَمْدِهِ

16. La ilaha illallohu vahdahu - 10/100 marta
لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ...

17. Subhanalloh va bihamdihi 'adada xalqih - 3 marta
سُبْحَانَ اللَّهِ وَبِحَمْدِهِ عَدَدَ خَلْقِهِ...

18. Astag'firulloh - 100 marta
أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ

19. Salavot - 10 marta
اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ
"""

KECHKI_ZIKR = """🌙 KECHKI ZIKRLAR - IDLIB

1. Oyatul Kursiy - 1 marta
اللَّهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَنْ ذَا الَّذِي يَشْفَعُ عِنْدَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ
Ma'nosi: Allohdan o'zga iloh yo'q, U tirik va bardavomdir. Uni uyqu ham, mudrash ham tutmaydi.

2. Ixlos, Falaq, Nos - har biri 3 martadan
Ixlos: قُلْ هُوَ اللَّهُ أَحَدٌ، اللَّهُ الصَّمَدُ، لَمْ يَلِدْ وَلَمْ يُولَدْ، وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ
Falaq: قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ، مِن شَرِّ مَا خَلَقَ، وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ، وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ، وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ
Nos: قُلْ أَعُوذُ بِرَبِّ النَّاسِ، مَلِكِ النَّاسِ، إِلَهِ النَّاسِ، مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ، الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ، مِنَ الْجِنَّةِ وَالنَّاسِ

3. Amsayna va amsal mulku lillah - 1 marta
أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ
Ma'nosi: Kechga kirdik, mulk ham Allohniki bo'lib kechga kirdi.

4. Allohumma bika amsayna - 1 marta
اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ الْمَصِيرُ
Ma'nosi: Allohim, Sening yordaming bilan kechga kirdik.

5. Sayyidul istig'for - 1 marta
اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي، فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ
Ma'nosi: Allohim, Sen mening Robbimsan, Sendan o'zga iloh yo'q.

6. Allohumma inni amsaytu ushhiduka - 4 marta
اللَّهُمَّ إِنِّي أَمْسَيْتُ أُشْهِدُكَ، وَأُشْهِدُ حَمَلَةَ عَرْشِكَ، وَمَلَائِكَتَكَ، وَجَمِيعَ خَلْقِكَ، أَنَّكَ أَنْتَ اللَّهُ لَا إِلَهَ إِلَّا أَنْتَ وَحْدَكَ لَا شَرِيكَ لَكَ، وَأَنَّ مُحَمَّدًا عَبْدُكَ وَرَسُولُكَ

7. Allohumma ma amsa bi - 1 marta
اللَّهُمَّ مَا أَمْسَى بِي مِنْ نِعْمَةٍ أَوْ بِأَحَدٍ مِنْ خَلْقِكَ فَمِنْكَ وَحْدَكَ لَا شَرِيكَ لَكَ، فَلَكَ الْحَمْدُ وَلَكَ الشُّكْرُ

8. Allohumma 'afini - 3 marta
اللَّهُمَّ عَافِنِي فِي بَدَنِي، اللَّهُمَّ عَافِنِي فِي سَمْعِي، اللَّهُمَّ عَافِنِي فِي بَصَرِي، لَا إِلَهَ إِلَّا أَنْتَ

9. Allohumma inni a'uzu bika - 3 marta
اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْكُفْرِ، وَالْفَقْرِ، وَأَعُوذُ بِكَ مِنْ عَذَابِ الْقَبْرِ، لَا إِلَهَ إِلَّا أَنْتَ

10. Hasbiyallohu - 7 marta
حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ، عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ

11. Bismillahilladhiy - 3 marta
بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ

12. Roziytu billahi - 3 marta
رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ نَبِيًّا

13. Ya Hayyu ya Qayyum - 1 marta
يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ، أَصْلِحْ لِي شَأْنِي كُلَّهُ، وَلَا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ

14. Amsayna 'ala fitratil Islam - 1 marta
أَمْسَيْنَا عَلَى فِطْرَةِ الْإِسْلَامِ، وَعَلَى كَلِمَةِ الْإِخْلَاصِ، وَعَلَى دِينِ نَبِيِّنَا مُحَمَّدٍ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ، وَعَلَى مِلَّةِ أَبِينَا إِبْرَاهِيمَ حَنِيفًا مُسْلِمًا وَمَا كَانَ مِنَ الْمُشْرِكِينَ

15. Subhanalloh va bihamdih - 100 marta
سُبْحَانَ اللَّهِ وَبِحَمْدِهِ

16. La ilaha illallohu vahdahu - 10/100 marta
لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ

17. Subhanalloh va bihamdihi 'adada xalqih - 3 marta
سُبْحَانَ اللَّهِ وَبِحَمْدِهِ عَدَدَ خَلْقِهِ، وَرِضَا نَفْسِهِ، وَزِنَةَ عَرْشِهِ، وَمِدَادَ كَلِمَاتِهِ

18. Astag'firulloh - 100 marta
أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ

19. Salavot - 10 marta
اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ

Alloh qabul qilsin.
"""

def get_namoz():
    try:
        r = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={CITY}&country={COUNTRY}&method=5", timeout=10).json()
        t = r["data"]["timings"]
        return f"""🕌 Idlib - Bugungi Namoz Vaqtları:

Bomdod: {t['Fajr'][:5]}
Quyosh: {t['Sunrise'][:5]}
Peshin: {t['Dhuhr'][:5]}
Asr: {t['Asr'][:5]}
Shom: {t['Maghrib'][:5]}
Xufton: {t['Isha'][:5]}"""
    except:
        return "Vaqtni olishda xato bo'ldi."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    await update.message.reply_text("Assalomu alaykum! 🤲\nPastdagi knopkani bosing:", reply_markup=KEYBOARD)
    await update.message.reply_text(get_namoz(), reply_markup=KEYBOARD)

async def knopka_bosildi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    text = update.message.text
    if text == "🕋 Namoz vaqtlari":
        await update.message.reply_text(get_namoz(), reply_markup=KEYBOARD)
    elif text == "🌅 Ertalabki zikrlar":
        await update.message.reply_text(ERTALABKI_ZIKR, reply_markup=KEYBOARD)
    elif text == "🌙 Kechki zikrlar":
        await update.message.reply_text(KECHKI_ZIKR, reply_markup=KEYBOARD)
    else:
        await update.message.reply_text("Pastdagi knopkani bosing 👇", reply_markup=KEYBOARD)

async def auto_yuborish(context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    if not CHAT_ID:
        return
    try:
        r = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={CITY}&country={COUNTRY}&method=5", timeout=10).json()
        t = r["data"]["timings"]
        now = datetime.now(TZ).strftime("%H:%M")
        if now == t['Fajr'][:5]:
            await context.bot.send_message(chat_id=CHAT_ID, text="🕌 Bomdod vaqti bo'ldi!\n\n" + ERTALABKI_ZIKR, reply_markup=KEYBOARD)
        elif now == t['Asr'][:5]:
            await context.bot.send_message(chat_id=CHAT_ID, text="🕌 Asr vaqti bo'ldi!\n\n" + KECHKI_ZIKR, reply_markup=KEYBOARD)
    except:
        pass

def main():
    keep_alive()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, knopka_bosildi))
    app.job_queue.run_repeating(auto_yuborish, interval=60, first=10)
    print("Bot ishga tushdi - knopkali + to'liq zikrli...")
    app.run_polling()

if __name__ == "__main__":
    main()
