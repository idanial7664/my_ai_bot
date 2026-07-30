import os
import telebot
import requests

# گرفتن کلیدها از متغیرهای محیطی
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

print(f"BOT_TOKEN: {'set' if BOT_TOKEN else 'NOT SET'}")
print(f"GROQ_API_KEY: {'set' if GROQ_API_KEY else 'NOT SET'}")

bot = telebot.TeleBot(BOT_TOKEN)

# آدرس API Groq
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_ai_response(text):
    """گرفتن پاسخ از Groq"""
    if not GROQ_API_KEY:
        return "❌ کلید API تنظیم نشده!"
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "تو یک دستیار فارسی هستی به اسم دانیال. مهربان و دوستانه جواب بده. فقط به فارسی جواب بده."},
                {"role": "user", "content": text}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
        
        return f"❌ خطا: {response.status_code}"
        
    except Exception as e:
        return f"❌ خطا: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    ai_reply = get_ai_response("سلام، خودت رو معرفی کن")
    bot.reply_to(message, ai_reply)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        print(f"Received: {message.text}")
        ai_reply = get_ai_response(message.text)
        bot.reply_to(message, ai_reply)
        print(f"Replied: {ai_reply[:100]}")
    except Exception as e:
        print(f"Error: {str(e)}")
        bot.reply_to(message, f"❌ خطا: {str(e)}")

print("🤖 Bot is running with Groq + Llama 3!")
bot.infinity_polling()
