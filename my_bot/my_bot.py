import os
import telebot # Library import ki
import datetime # date import ke liye 
import random
import wikipedia
import yt_dlp

# Step 1 wala Token yaha daalo (quotes ke andar)
TOKEN = os.environ.get('MY_TOKEN')

bot = telebot.TeleBot(TOKEN)

# 1. Start command ka reply
# Jab koi '/start' click karega to ye function chalega
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # 1. Ek khali Keyboard banao
    # 'resize_keyboard=True' se buttons chote aur sundar dikhenge
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # 2. Buttons create karo
    btn1 = telebot.types.KeyboardButton('Toss')
    btn2 = telebot.types.KeyboardButton('Password')
    btn3 = telebot.types.KeyboardButton('Date')
    btn4 = telebot.types.KeyboardButton('wiki India')
    
    # 3. Buttons ko keyboard mein add karo
    markup.add(btn1, btn2, btn3, btn4)
    
    # 4. Message ke saath keyboard bhejo ('reply_markup' parameter use karke)
    bot.reply_to(message, "Namaste Raj! Main taiyaar hu. Niche buttons se option chuno:", reply_markup=markup)

# 2. Smart Auto-Reply logic
# Ye function har text message ko padhega
@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    user_text = message.text.lower() # User ki baat ko lowercase me convert kiya taki match ho sake

    if "hello" in user_text or "hi" in user_text:
        bot.reply_to(message, "Hello Bhai! Kese ho?")

    elif "date" in user_text or "taarik" in user_text:
       aaj = datetime.datetime.now()
       date_text = aaj.strftime("%d-%m-%y")
       bot.reply_to(message, "Aaj ki date hai : " + date_text)
    
    elif "toss" in user_text or "sikka" in user_text:
        sikke_ke_pehlu = ["Head", "Tail"]
        nateeja = random.choice(sikke_ke_pehlu) # random choice ke liye 
        bot.reply_to(message, "sikka ghoom raha hai... Aya hai: " + nateeja)
    
    elif "password" in user_text or "pass" in user_text:
        # Step 1: Kahan se letters chunne hain (Raw Material)
        # Hum saare letters, numbers aur symbols ek jagah likh lenge
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        
        # Step 2: Khali password banaya
        my_password = ""
        
        # Step 3: Loop (10 baar chalega) -> C++ wala 'for loop'
        for i in range(12):  # 12 digits ka password banega
            my_password += random.choice(chars)
            
        # Step 4: User ko bhejo
        bot.reply_to(message, "Ye lo apka strong password: " + my_password)
        bot.reply_to(message, "(Isse yaad kar lena, main save nahi rakhta!)")

    elif "wiki" in user_text:
        # Step 1: Query saaf ki aur Title case kiya (india -> India)
        query = user_text.replace("wiki", "").strip().title()
        
        bot.reply_to(message, "Wikipedia par dhund raha hu... 🔍")
        
        try:
            # Step 2: Summary mangwai
            result = wikipedia.summary(query, sentences=2)
            bot.reply_to(message, result)
            
        except wikipedia.exceptions.DisambiguationError:
            # Jab confusion ho (Bahut sare options)
            bot.reply_to(message, "Thoda confusion hai. Bahut saare topics mil rahe hain. Thoda clear likho (Jaise: 'India Country' ya 'Virat Kohli').")
            
        except wikipedia.exceptions.PageError:
            # Jab page hi na mile
            bot.reply_to(message, "Ye topic Wikipedia par nahi mila. Spelling check karo!")
            
        except Exception as e:
            # Koi aur anjaan error
            bot.reply_to(message, "Kuch error aaya hai:  " + str(e))
    # --- YouTube Downloader Logic ---
    # Ye check karega ki kya message me youtube ka link hai?
    elif "youtube.com" in user_text or "youtu.be" in user_text:
        url = message.text
        
        bot.reply_to(message, "Video mil gaya! Download kar raha hu... ⏳\n(Isme thoda time lag sakta hai)")

        try:
            # 1. Video download karne ki settings
            # 1. Video download karne ki settings (Updated for White Screen Fix)
            ydl_opts = {
                'format': '18/best[ext=mp4]',  # Format 18 sabse safe hai (360p MP4)
                'outtmpl': 'video.mp4',
                'noplaylist': True,
                # Ye line YouTube ko confusing formats bhejne se rokegi
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
            }

            # 2. Asli download shuru
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # 3. User ko batao ki upload ho raha hai
            bot.reply_to(message, "Download complete! Ab Telegram par upload kar raha hu... 🚀")

            # 4. Video bhejo
            video_file = open('video.mp4', 'rb') # File kholo
            bot.send_video(message.chat.id, video_file, timeout=60)
            video_file.close() # File band karo

            # 5. Safai Abhiyaan (Delete file)
            os.remove('video.mp4') 
            
        except Exception as e:
            bot.reply_to(message, "Download fail ho gaya. Shayad video lamba hai ya link galat hai.")
            print("Error:", e) # Terminal me error dekhne ke liye

    elif "kaise ho" in user_text:
        bot.reply_to(message, "Main ek code hu, hamesha badhiya! Tum sunao?")
        
    elif "python" in user_text:
        bot.reply_to(message, "Python meri favorite language hai!")

    else:
        # Agar kuch samajh na aaye, to wahi baat wapas bol do (Echo)
        bot.reply_to(message, "Mujhe abhi iska jawab nahi pata, par tumne kaha: " + message.text)
    

 

# 3. Bot ko chalu rakhna (Loop)
print("Bot start ho gaya hai...")
bot.infinity_polling() # yeh code ko marne ni deta loop me rakhta hai