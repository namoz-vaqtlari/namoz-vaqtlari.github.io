import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

def get_prayer_times():
    try:
        url = "https://api.aladhan.com/v1/timingsByCity?city=Idlib&country=Syria&method=13"
        r = requests.get(url, timeout=10).json()
        t = r["data"]["timings"]
        hijri = r["data"]["date"]["hijri"]
        return (
            f"Namoz vaqtlari - Fu'ah / Idlib\n"
            f"Hijriy: {hijri['day']} {hijri['month']['en']} {hijri['year']}\n\n"
            f"Bomdod: {t['Fajr']}\n"
            f"Quyosh: {t['Sunrise']}\n"
            f"Peshin: {t['Dhuhr']}\n"
            f"Asr: {t['Asr']}\n"
            f"Shom: {t['Maghrib']}\n"
            f"Xufton: {t['Isha']}\n\n"
            f"Alloh ibodatlaringni qabul qilsin!"
        )
    except Exception as e:
        return f"Xatolik: {e}"

MORNING_1 = "ERTALABKI ZIKRLAR - 1-qism\n\n"
MORNING_1 += "1. OYATAL KURSIY (1 marta)\n"
MORNING_1 += "Allohu la ilaha illa huwal hayyul qoyyum, la ta'xuzuhu sinatuv va la navm, lahu ma fis samavati va ma fil ard, man zallazi yashfa'u 'indahu illa bi iznih, ya'lamu ma bayna aydihim va ma xolfahum, va la yuhituna bi shay'im min 'ilmihi illa bima sha', vasi'a kursiyyuhus samavati val ard, va la ya'uduhu hifzuhuma, va huwal 'aliyyul 'azim.\n\n"
MORNING_1 += "2. IXLOS, FALAQ, NOS - 3 martadan\n"
MORNING_1 += "Qul huvallohu ahad...\nQul a'uzu birobbil falaq...\nQul a'uzu birobbin nas...\n\n"
MORNING_1 += "3. ASBAHNA VA ASBAHAL MUL
