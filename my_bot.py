import os
import telebot
from flask import Flask
import threading
import datetime
import random
import wikipedia
import yt_dlp
import google.generativeai as genai  # <--- NEW: AI Library

# --- SETUP ---
TOKEN = os.environ.get('MY_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- AI SETUP (Google Gemini) ---
GEMINI_KEY = os.environ.get('GEMINI_KEY')
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Ye fast aur free model hai

# --- 1. START COMMAND (BUTTONS) ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Toss')
    btn2 = telebot.types.KeyboardButton('Password')
    btn3 = telebot.types.KeyboardButton('Date')
    btn4 = telebot.types.KeyboardButton('wiki India')
    markup.add(btn1, btn2, btn3, btn4)
    bot.reply_to(message, "Namaste Raj! Main AI Bot hu. Mujhse kuch bhi pucho!", reply_markup=markup)

# --- 2. MAIN LOGIC (AUTO REPLY) ---
@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    user_text = message.text.lower()

    # --- Greeting ---
    if "hello" in user_text or "hi" in user_text:
        bot.reply_to(message, "Hello Bhai! Kese ho?")

    # --- Date Feature ---
    elif "date" in user_text or "taarik" in user_text:
        aaj = datetime.datetime.now()
        date_text = aaj.strftime("%d-%m-%y")
        bot.reply_to(message, "Aaj ki date hai : " + date_text)
    
    # --- Toss Feature ---
    elif "toss" in user_text or "sikka" in user_text:
        sikke_ke_pehlu = ["Head", "Tail"]
        nateeja = random.choice(sikke_ke_pehlu)
        bot.reply_to(message, "Sikka ghoom raha hai... Aya hai: " + nateeja)
    
    # --- Password Feature ---
    elif "password" in user_text or "pass" in user_text:
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        my_password = ""
        for i in range(12):
            my_password += random.choice(chars)
        bot.reply_to(message, "Ye lo apka strong password: " + my_password)

    # --- Wikipedia Feature ---
    elif "wiki" in user_text:
        query = user_text.replace("wiki", "").strip().title()
        bot.reply_to(message, "Wikipedia par dhund raha hu... 🔍")
        try:
            result = wikipedia.summary(query, sentences=2)
            bot.reply_to(message, result)
        except Exception as e:
            bot.reply_to(message, "Error aaya: " + str(e))

    # --- YouTube Downloader Feature ---
    elif "youtube.com" in user_text or "youtu.be" in user_text:
        url = message.text
        bot.reply_to(message, "Video mil gaya! Download kar raha hu... ⏳")
        try:
            ydl_opts = {
                'format': '18/best[ext=mp4]',
                'outtmpl': 'video.mp4',
                'noplaylist': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            bot.reply_to(message, "Uploading... 🚀")
            video_file = open('video.mp4', 'rb')
            bot.send_video(message.chat.id, video_file, timeout=60)
            video_file.close()
            os.remove('video.mp4')
        except Exception as e:
            bot.reply_to(message, "Download fail. Error: " + str(e))

    # --- AI BRAIN (Agar kuch match na ho, to Google se pucho) ---
    else:
        # User ko batao ki AI soch raha hai
        bot.send_chat_action(message.chat.id, 'typing')
        
        try:
            # Google Gemini ko message bhejo
            response = model.generate_content(message.text)
            # Jawab wapas user ko bhejo
            bot.reply_to(message, response.text)
        except Exception as e:
            bot.reply_to(message, "Sorry, AI abhi busy hai. Error: " + str(e))


# --- 3. FAKE SERVER FOR RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "I am alive"

def run_web_server():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web_server)
    t.start()

# --- 4. EXECUTION ---
print("Bot start ho raha hai...")
keep_alive()
bot.infinity_polling()


