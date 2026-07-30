import os
import telebot
import requests
import json

# گرفتن کلیدها از متغیرهای محیطی
BOT_TOKEN = os.environ.get('BOT_TOKEN')
HF_TOKEN = os.environ.get('HF_TOKEN')

print(f"BOT_TOKEN: {'set' if BOT_TOKEN else 'NOT SET'}")
print(f"HF_TOKEN: {'set' if HF_TOKEN else 'NOT SET'}")

# راه‌اندازی بات تلگرام
bot = telebot.TeleBot(BOT_TOKEN)

# مدل‌های مختلف برای امتحان
MODELS = [
    "mistralai/Mistral-7B-Instruct-v0.3",
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "microsoft/DialoGPT-medium"
]

# تابع پاسخگویی
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        print(f"Received: {message.text}")
        
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        # امتحان مدل‌های مختلف
        for model in MODELS:
            try:
                payload = {
                    "inputs": f"<s>[INST] {message.text} [/INST]",
                    "parameters": {"max_new_tokens": 300, "temperature": 0.7}
                }
                
                response = requests.post(
                    f"https://api-inference.huggingface.co/models/{model}",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        reply = data[0].get('generated_text', '')
                        if '[/INST]' in reply:
                            reply = reply.split('[/INST]')[-1].strip()
                        if reply:
                            bot.reply_to(message, reply[:2000])
                            return
                
                # اگه مدل load نشده، صبر کن
                if response.status_code == 503:
                    print(f"Model {model} loading, trying next...")
                    continue
                    
            except Exception as e:
                print(f"Error with {model}: {str(e)}")
                continue
        
        # اگه هیچ مدلی کار نکرد
        bot.reply_to(message, "❌ مدل‌ها در حال حاضر در دسترس نیستن. لطفاً بعداً امتحان کن.")
            
    except Exception as e:
        print(f"Exception: {str(e)}")
        bot.reply_to(message, f"❌ خطا: {str(e)}")

# اجرای ربات
print("🤖 Bot is running...")
bot.infinity_polling()
