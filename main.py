import pandas as pd
from datetime import datetime, date
import requests
import os

# ⚙️ Sozlamalar
BOT_TOKEN = "BOT TOKEN"
CHAT_IDS = ["ID",# Kanal
            ""]

# 📁 Fayl 
EXCEL_FILE = r"C:\Users\admin\Desktop\TOM xodimlari tug'ilgan kunlari/tabrik.xlsx"
PHOTO_DIR = r"C:\Users\admin\Desktop\TOM xodimlari tug'ilgan kunlari/Photos"

# 🖼 Bayramlar uchun rasm va matnlar
BAYRAMLAR = {
    "01-01": {
        "text": "🎉 Yangi yil bilan!",
        "image": "newyear.jpg"
    },
    "01-14": {
        "text": "🛡 Vatan himoyachilari kuni bilan barchalaringizni muborakbot etamiz!",
        "image": "army_day.jpg"
    },
     "02-07": {
        "text": "uz Bugun O'zbekiston Respublikasi Gerbi qabul qilingan kun!",
        "image": "gerb_day.jpg"
    },
    "03-08": {
        "text": "🌸 8-mart — Xotin-qizlar bayrami bilan! Mutabar onalarimiz Munis opa singillarimizni bayramlari bilan tabriklaymiz",
        "image": "women_day.jpg"
    },
    "03-21": {
        "text": """Sizni yurtimizning yangilanish fasli bahor hamda ajoyib bayram Navro`z ayyomi bilan chin dildan qutlayman! Ushbu kunda sizni quvonch va shodlik tark etmasin! Yurtimiz O`zbekistonning yangi yilida yangi orzularingiz amalga oshsin! Bugungi Navro`z ayyomini ko`tarinki kayfiyatda o`tkazishingizni tilab qolaman! Yana bir bor Navro`z ayyomi muborak bo`lsin!

Ezgu tilaklarim guldasta bo`lsin,
Dildagi so`zlarim dildasta bo`lsin.
Baxt va omad sizga payvasta bo`lsin,
Bugungi bayramingiz muborak bo’`sin!
Navro`z bayrami muborak!!!

Azizam baxt iqbol doim yor bo`lsin,
Yurgan yo`llaringiz gullarga to`lsin.
Omadingiz ko`rib ko`zlar quvonsin,
Navro`z ayyomingiz muborak bo`lsin!,""",

       "image": "navruz.jpg"
    },
     "06-30": {
        "text": """Siz, azizlarni bugungi yoshlik, baxt va nafosat ayyomi bilan yana bir bor chin dildan tabriklab, barchangizga sihat-salomatlik, ulkan yutuq va omadlar tilayman.

Hech qachon unutmang, g‘alaba va baxt – astoydil intilganniki!

Sizlarning yutug‘ingiz – bu butun el-yurtimizning yutug‘i.

Xalqimiz sizlarga ishonadi, sizlarga tayanadi, sizlardan kuch-g‘ayrat, ruh va ilhom oladi.

O‘z oldingizga ulug‘ maqsadlar qo‘yib yashashdan aslo charchamang!

Yangi O‘zbekistonni albatta sizlar bilan, butun mamlakatimiz yoshlari bilan birga barpo etamiz.

Barchangizga bayram muborak bo‘lsin, qadrli o‘g‘il-qizlarim!!

Shavkat Mirziyoyev,
O‘zbekiston Respublikasi Prezidenti""",
        "image": "yoshlar_day.jpg"
    },
    "05-09": {
        "text": "🕊 Xotira va qadrlash kuni bilan!",
        "image": "memory_day.jpg"
    },
    "09-01": {
        "text": "🇺🇿 Mustaqillik bayrami bilan!",
        "image": "Mustaqillik.jpg"
    },
    "10-01": {
        "text": "📚 Ustoz va murabbiylar kuni bilan!",
        "image": "teachers_day.jpg"
    },
    "11-21": {
        "text": "📚 Davlat tiliga o'zbek tili maqomi berilgan kun bilan barcha jamoadoshlarimizni tabriklayman!",
        "image": "til_day.jpg"
    },
    "12-08": {
        "text": "📜 Konstitutsiya kuni bilan!",
        "image": "constitution_day.jpg"
    },
    "12-31": {
        "text": "🎆 Yangi yil arafasi bilan!",
       # "image": "newyear_eve.jpg"
    }
}

# 🧮 Yosh hisoblash funksiyasi
def yosh_hisobla(tugilgan_sana):
    bugun = date.today()
    return bugun.year - tugilgan_sana.year - ((bugun.month, bugun.day) < (tugilgan_sana.month, tugilgan_sana.day))

# 📤 Telegramga rasm yuborish
def rasm_yuborish(text, image_path):
    for chat_id in CHAT_IDS:
        with open(image_path, 'rb') as img:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                data={"chat_id": chat_id, "caption": text},
                files={"photo": img}
            )

# 🔁 Asosiy jarayon
try:
    bugun = datetime.now().strftime("%m-%d")
    hafta_kuni = datetime.now().weekday()  # 0=Monday, 6=Sunday

    # 🔔 Bayram tabrigi (sendPhoto va sendMessage qismini ham siklga oling)
    try:
        if bugun in BAYRAMLAR:
            bayram = BAYRAMLAR[bugun]
            bayram_text = f"""{bayram['text']}
\nBarchangizni ushbu bayram bilan chin yurakdan tabriklaymiz! 🎉\n\nHurmat bilan,\n TOM jamoasi!"""

            image_path = os.path.join(PHOTO_DIR, bayram.get('image', '')) if 'image' in bayram else None
            for chat_id in CHAT_IDS:
                if image_path and os.path.isfile(image_path):
                    resp = requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                        data={"chat_id": chat_id, "caption": bayram_text},
                        files={"photo": open(image_path, 'rb')}
                    )
                    print("sendPhoto javobi:", resp.text)
                else:
                    resp = requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        data={"chat_id": chat_id, "text": bayram_text}
                    )
                    print("sendMessage javobi:", resp.text)
            print("✅ Bayram tabrigi yuborildi!")
    except Exception as e:
        print(f"❌ Bayram tabrigi xatoligi: {e}")

    # 📂 Tug‘ilgan kunlar
    try:
        df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
        df["Tugilgan_sana"] = pd.to_datetime(df["Tugilgan_sana"], errors='coerce')
        df["mm-dd"] = df["Tugilgan_sana"].dt.strftime("%m-%d")
        bugungi = df[df["mm-dd"] == bugun]

        if not bugungi.empty:
            rows = []
            for _, row in bugungi.iterrows():
                yosh = yosh_hisobla(row["Tugilgan_sana"])
                rows.append(f"🎉 {row['Ism']} — {row['Lavozim']} (🎂 {yosh} yosh)")

            ism_matni = "\n".join(rows)
            birthday_photo = os.path.join(PHOTO_DIR, f"birthday_{(hafta_kuni % 7) + 1}.jpg")

            if len(rows) == 1:
                ism = rows[0]
                text = f"""🎉 Hurmatli!:\n\n{ism}

💐       {bugungi.iloc[0]['Ism']}!
TOM jamoasi nomidan sizni bugungi tug‘ilgan kuningiz bilan samimiy tabriklaymiz!
Yangi yoshingiz sizga baxt, omad, mustahkam sog‘liq va yorqin yutuqlar olib kelsin!
Har bir tongingiz ilhom bilan, har bir kuningiz esa zavq bilan o‘tsin!

Hurmat bilan,
TOM jamoasi 💼"""
            else:
                text = f"""🎉 Bugungi tug‘ilgan kun egalari:\n\n{ism_matni}

💐
TOM jamoasi sizlarni bugungi quvonchli kuningiz bilan chin dildan tabriklaydi!
Yangi yoshingiz sizga mustahkam sog‘liq, oilaviy baxt, katta yutuqlar va ezgu orzularingiz ro‘yobini olib kelsin.
Har bir kuningiz farovonlik va muvaffaqiyat bilan to‘lsin!

Hurmat bilan,
TOM jamoasi 💼"""

            rasm_yuborish(text, birthday_photo)
            print("✅ Tug‘ilgan kun tabrigi yuborildi!")
        else:
            print("ℹ️ Bugun tug‘ilgan kun yo‘q.")
    except Exception as e:
        print(f"❌ Tug‘ilgan kun tabrigi xatoligi: {e}")

except Exception as e:
    print(f"❌ Umumiy xatolik: {e}")
import time

# O'zingizning Telegram user ID raqamingizni shu yerga yozing
ADMIN_USER_ID = 1046430086  # <-- O'zingizning ID raqamingizni yozing

def faqat_admin_xabarini_kanalga_yuborish():
    offset = None
    while True:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        if offset:
            url += f"?offset={offset}"
        resp = requests.get(url).json()
        for update in resp.get("result", []):
            offset = update["update_id"] + 1
            if "message" in update and "text" in update["message"]:
                user_id = update["message"]["from"]["id"]
                user_text = update["message"]["text"]
                if user_id == ADMIN_USER_ID:
                    # Faqat siz yozgan xabar barcha chatlarga yuboriladi
                    for chat_id in CHAT_IDS:
                        requests.post(
                            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                            data={"chat_id": chat_id, "text": user_text}
                        )
        time.sleep(2)

# Pastga qo'shing (asosiy jarayon tugagandan so'ng):
faqat_admin_xabarini_kanalga_yuborish()
