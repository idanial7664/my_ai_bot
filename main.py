import os
import telebot
import requests
import json
import time

# گرفتن کلیدها از متغیرهای محیطی
BOT_TOKEN = os.environ.get('BOT_TOKEN')
HF_TOKEN = os.environ.get('HF_TOKEN')

print(f"BOT_TOKEN: {'set' if BOT_TOKEN else 'NOT SET'}")
print(f"HF_TOKEN: {'set' if HF_TOKEN else 'NOT SET'}")

# راه‌اندازی بات تلگرام
bot = telebot.TeleBot(BOT_TOKEN)

# مدل‌های سبک و مطمئن (همیشه در دسترس)
MODELS = [
    "microsoft/DialoGPT-medium",
    "microsoft/DialoGPT-small",
    "facebook/opt-350m",
]

# تابع پاسخگویی
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! 👋\nمن ربات هوش مصنوعی تو هستم.\nهر سوالی بپرس جواب میدم!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        print(f"Received: {message.text}")
        
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        # امتحان مدل‌های مختلف
        for model in MODELS:
            try:
                print(f"Trying model: {model}")
                
                # فرمت ساده برای DialoGPT
                if "DialoGPT" in model:
                    payload = {
                        "inputs": message.text,
                        "parameters": {
                            "max_new_tokens": 200,
                            "temperature": 0.7,
                            "do_sample": True
                        }
                    }
                else:
                    payload = {
                        "inputs": message.text,
                        "parameters": {"max_new_tokens": 200}
                    }
                
                response = requests.post(
                    f"https://api-inference.huggingface.co/models/{model}",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        reply = data[0].get('generated_text', '')
                        if reply and reply != message.text:
                            bot.reply_to(message, reply[:2000])
                            return
                
                if response.status_code == 503:
                    print(f"Model {model} loading...")
                    time.sleep(2)
                    continue
                    
            except Exception as e:
                print(f"Error with {model}: {str(e)}")
                continue
        
        # پیام پیش‌فرض
        bot.reply_to(message, "🤖 سلام! من هنوز در حال یادگیری هستم.\nلطفاً بعداً دوباره امتحان کن.")
            
    except Exception as e:
        print(f"Exception: {str(e)}")
        bot.reply_to(message, f"❌ خطا: {str(e)}")

# اجرای ربات
print("🤖 Bot is running...")
bot.infinity_polling()
