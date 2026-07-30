import os
import telebot
import requests

# گرفتن کلیدها از متغیرهای محیطی
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

# راه‌اندازی بات تلگرام
bot = telebot.TeleBot(BOT_TOKEN)

# آدرس API Gemini (OpenAI-compatible)
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# تابع پاسخگویی
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        # ارسال درخواست به Gemini API
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            "contents": [{
                "parts": [{"text": message.text}]
            }]
        }
        
        response = requests.post(
            f"{API_URL}?key={GEMINI_KEY}",
            headers=headers,
            json=payload
        )
        
        data = response.json()
        
        if 'candidates' in data and len(data['candidates']) > 0:
            reply = data['candidates'][0]['content']['parts'][0]['text']
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, "❌ خطا: پاسخی دریافت نشد")
            
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {str(e)}")

# اجرای ربات
print("🤖 Bot is running...")
bot.infinity_polling()
