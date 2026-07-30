import os
import telebot
import requests
import json
import random

# گرفتن کلیدها از متغیرهای محیطی
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ROUTER_API_KEY = os.environ.get('ROUTER_API_KEY')

print(f"BOT_TOKEN: {'set' if BOT_TOKEN else 'NOT SET'}")
print(f"ROUTER_API_KEY: {'set' if ROUTER_API_KEY else 'NOT SET'}")

bot = telebot.TeleBot(BOT_TOKEN)

# آدرس API 9router (OpenAI-compatible)
ROUTER_API_URL = "https://9router-production-2e07.up.railway.app/v1/chat/completions"

# پاسخ‌های آماده
FALLBACK_RESPONSES = {
    "سلام": ["سلام! خوش اومدی! 😊", "سلام دوست من! چطوری؟"],
    "حالت چطوره": ["ممنون، خوبم! تو چطوری؟ 😊"],
    "اسم چیه": ["من دانیال هستم، دستیار هوش مصنوعی تو! 🤖"],
    "کی هستی": ["من یه ربات هوش مصنوعی هستم! 🤖"],
    "خداحافظ": ["خداحافظ! موفق باشی! 👋"],
}

def get_ai_response(text):
    """گرفتن پاسخ از 9router"""
    if not ROUTER_API_KEY:
        print("ROUTER_API_KEY not set!")
        return None
    
    try:
        headers = {
            "Authorization": f"Bearer {ROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mimo",
            "messages": [
                {"role": "system", "content": "تو یک دستیار فارسی هستی به اسم دانیال. مهربان و دوستانه جواب بده."},
                {"role": "user", "content": text}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        print(f"Calling 9router API...")
        response = requests.post(
            ROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
        
        print(f"Error: {response.text[:200]}")
        return None
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def get_fallback_response(text):
    """پاسخ آماده"""
    text_lower = text.lower().strip()
    for key, responses in FALLBACK_RESPONSES.items():
        if key in text_lower:
            return random.choice(responses)
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! 👋\nمن دانیال هستم، ربات هوش مصنوعی تو!\nبا 9router و Mimo کار می‌کنم! 🤖\nهر سوالی بپرس جواب میدم!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        print(f"Received: {message.text}")
        
        # AI رو امتحان کن
        ai_reply = get_ai_response(message.text)
        
        if ai_reply:
            bot.reply_to(message, ai_reply)
            print(f"AI Reply: {ai_reply[:100]}")
        else:
            # پاسخ آماده
            fallback = get_fallback_response(message.text)
            if fallback:
                bot.reply_to(message, fallback)
            else:
                bot.reply_to(message, "🤖 ممنون از پیامت! من هنوز در حال یادگیری هستم.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        bot.reply_to(message, "🤖 ممنون از پیامت!")

print("🤖 Bot is running with 9router + Mimo!")
bot.infinity_polling()
