import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

# --- Namoz vaqtlari ---
def get_prayer_times():
    try:
        url = "https://api.aladhan.com/v1/timingsByCity?city=Idlib&country=Syria&method=13"
        r = requests.get(url, timeout=10).json()
        t = r["data"]["timings"]
        hijri = r["data"]["date"]["hijri"]
        return (
            f"🕌 *Namoz vaqtlari -  / Idlib*\n"
            f"📅 Hijriy: {hijri['day']} {hijri['month']['en']} {hijri['year']}\n\n"
            f"🌅 Bomdod: {t['Fajr']}\n"
            f"☀️ Quyosh: {t['Sunrise']}\n"
            f"🕐 Peshin: {t['Dhuhr']}\n"
            f"🌤️ Asr: {t['Asr']}\n"
            f"🌇 Shom: {t['Maghrib']}\n"
            f"🌙 Xufton: {t['Isha']}\n\n"
            f"🤲 Alloh ibodatlaringni qabul qilsin!"
        )
    except Exception as e:
        return f"Xatolik: {e}"

# --- TO'LIQ ZIKRLAR ---
MORNING_1 = """🌅 ERTALABKI ZIKRLAR - 1-qism

1. OYATAL KURSIY (1 marta)
Allohu la ilaha illa huwal hayyul qoyyum, la ta'xuzuhu sinatuv va la navm, lahu ma fis samavati va ma fil ard, man zallazi yashfa'u 'indahu illa bi iznih, ya'lamu ma bayna aydihim va ma xolfahum, va la yuhituna bi shay'im min 'ilmihi illa bima sha', vasi'a kursiyyuhus samavati val ard, va la ya'uduhu hifzuhuma, va huwal 'aliyyul 'azim.

2. IXLOS, FALAQ, NOS - 3 martadan
Qul huvallohu ahad...
Qul a'uzu birobbil falaq...
Qul a'uzu birobbin nas...

3. ASBAHNA VA ASBAHAL MULKU LILLAH
Asbahna va asbahal mulku lillah, val hamdu lillah, la ilaha illallohu vahdahu la sharika lah, lahul mulku va lahul hamdu va huva 'ala kulli shay'in qodir. Robbi as'aluka xoyro ma fi hazal yavmi va xoyro ma ba'dah, va a'uzu bika min sharri ma fi hazal yavmi va sharri ma ba'dah. Robbi a'uzu bika minal kasali va su'il kibar. Robbi a'uzu bika min 'azabin fin nar va 'azabin fil qobr.

4. ALLOHUMMA BIKA ASBAHNA
Allohumma bika asbahna va bika amsayna va bika nahya va bika namutu va ilaykan nushur.

5. SAYYIDUL ISTIG'FOR (1 marta)
Allohumma anta Robbi, la ilaha illa anta, xolaqtani va ana 'abduka, va ana 'ala 'ahdika va va'dika mastato'tu, a'uzu bika min sharri ma sona'tu, abu'u laka bini'matika 'alayya, va abu'u bizanbi, fag'fir li, fa innahu la yag'firuz zunuba illa anta.
"""

MORNING_2 = """🌅 ERTALABKI ZIKRLAR - 2-qism

6. ALLOHUMMA INNI AS'ALUKA
Allohumma inni as'alukal 'afva val 'afiyata fid dunya val oxiroh. Allohumma inni as'alukal 'afva val 'afiyata fi diniy va dunyaya va ahliy va maliy. Allohummastur 'avrotiy va amin rav'otiy. Allohummahfazniy min bayni yadayya va min xolfiy va 'an yaminiy va 'an shimaliy va min favqiy, va a'uzu bi'azomatika an ug'tala min tahtiy.

7. HASBIYALLOHU - 7 marta
Hasbiyallohu la ilaha illa Huva, 'alayhi tavakkaltu va Huva Robbul 'arshil 'azim.

8. BISMILLAHILLAZI - 3 marta
Bismillahillazi la yadurru ma'asmihi shay'un fil ardi va la fis sama', va Huwas sami'ul 'alim.

9. RODITU BILLAHI - 3 marta
Roditu billahi Robban, va bil islami dinan, va bi Muhammadin sollallohu 'alayhi va sallam nabiyyan.

10. YA HAYYU YA QOYYUM
Ya Hayyu Ya Qoyyum, birohmatika astag'isu, aslih li sha'ni kullah, va la takilniy ila nafsiy torfata 'ayn.

11. SUBHANOLLOHI VA BIHAMDIHI - 100 marta
Subhanallohi va bihamdihi

12. LA ILAHA ILLALLOH - 100 marta
La ilaha illallohu vahdahu la sharika lah, lahul mulku va lahul hamdu va Huva 'ala kulli shay'in Qodir.

13. ASTAG'FIRULLOH - 100 marta

🤲 kuningiz xayrli bo'lsin!
"""

EVENING_1 = """🌙 KECHKI ZIKRLAR - 1-qism

1. OYATAL KURSIY (1 marta)
Allohu la ilaha illa huwal hayyul qoyyum, la ta'xuzuhu sinatuv va la navm, lahu ma fis samavati va ma fil ard, man zallazi yashfa'u 'indahu illa bi iznih, ya'lamu ma bayna aydihim va ma xolfahum, va la yuhituna bi shay'im min 'ilmihi illa bima sha', vasi'a kursiyyuhus samavati val ard, va la ya'uduhu hifzuhuma, va huwal 'aliyyul 'azim.

2. IXLOS, FALAQ, NOS - 3 martadan
Qul huvallohu ahad...
Qul a'uzu birobbil falaq...
Qul a'uzu birobbin nas...

3. AMSAYNA VA AMSAL MULKU LILLAH
Amsayna va amsal mulku lillah, val hamdu lillah, la ilaha illallohu vahdahu la sharika lah, lahul mulku va lahul hamdu va huva 'ala kulli shay'in qodir. Robbi as'aluka xoyro ma fi hazihil laylati va xoyro ma ba'daha, va a'uzu bika min sharri ma fi hazihil laylati va sharri ma ba'daha. Robbi a'uzu bika minal kasali va su'il kibar. Robbi a'uzu bika min 'azabin fin nar va 'azabin fil qobr.

4. ALLOHUMMA BIKA AMSAYNA
Allohumma bika amsayna va bika asbahna va bika nahya va bika namutu va ilaykal masiyr.

5. SAYYIDUL ISTIG'FOR (1 marta)
Allohumma anta Robbi, la ilaha illa anta, xolaqtani va ana 'abduka, va ana 'ala 'ahdika va va'dika mastato'tu, a'uzu bika min sharri ma sona'tu, abu'u laka bini'matika 'alayya, va abu'u bizanbi, fag'fir li, fa innahu la yag'firuz zunuba illa anta.
"""

EVENING_2 = """🌙 KECHKI ZIKRLAR - 2-qism
