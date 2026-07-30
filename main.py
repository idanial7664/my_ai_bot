import os
import telebot
import google.generativeai as genai

# گرفتن کلیدها از متغیرهای محیطی
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

# راه‌اندازی بات تلگرام
bot = telebot.TeleBot(BOT_TOKEN)

# راه‌اندازی Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# تابع پاسخگویی
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {str(e)}")

# اجرای ربات
print("🤖 Bot is running...")
bot.infinity_polling()
