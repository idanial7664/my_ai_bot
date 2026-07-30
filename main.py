import os
import telebot
import requests
import random

# گرفتن کلیدها از متغیرهای محیطی
BOT_TOKEN = os.environ.get('BOT_TOKEN')
HF_TOKEN = os.environ.get('HF_TOKEN')

print(f"BOT_TOKEN: {'set' if BOT_TOKEN else 'NOT SET'}")
print(f"HF_TOKEN: {'set' if HF_TOKEN else 'NOT SET'}")

bot = telebot.TeleBot(BOT_TOKEN)

# پاسخ‌های آماده (فوق‌العاده ساده و مطمئن)
SMART_RESPONSES = {
    "سلام": ["سلام! خوش اومدی! 😊", "سلام دوست من! چطوری؟", "سلام! حالت چطوره؟"],
    "حالت چطوره": ["ممنون، خوبم! تو چطوری؟ 😊", "عالیم! ممنون که پرسیدی.", "خوبم ممنون! تو چخبر؟"],
    "اسم چیه": ["من دانیال هستم، دستیار هوش مصنوعی تو! 🤖", "اسم من دانیاله! 😊"],
    "کی هستی": ["من یه ربات هوش مصنوعی هستم که توسط هرمس ساخته شدم! 🤖", "من دانیال، دستیار تو هستم!"],
    "ممنون": ["خواهش میکنم! 😊", "قابلی نداشت! 💪", "خوشحالم کمکتون کردم!"],
    "خداحافظ": ["خداحافظ! موفق باشی! 👋", "بای بای! روز خوبی داشته باشی! 😊"],
}

# تابع پاسخ هوشمند
def smart_reply(text):
    text_lower = text.lower().strip()
    
    # چک کردن پاسخ‌های آماده
    for key, responses in SMART_RESPONSES.items():
        if key in text_lower:
            return random.choice(responses)
    
    # اگه پیدا نشد، از AI استفاده کن
    if HF_TOKEN:
        try:
            headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            payload = {
                "inputs": text,
                "parameters": {"max_new_tokens": 150, "temperature": 0.8}
            }
            
            response = requests.post(
                "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                headers=headers, json=payload, timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    ai_reply = data[0].get('generated_text', '')
                    if ai_reply and ai_reply != text and len(ai_reply) > 5:
                        return ai_reply[:500]
        except:
            pass
    
    # پاسخ پیش‌فرض
    return f"🤖 من متوجه شدم! ولی هنوز دارم یاد میگیرم. سوال دیگه‌ای داری؟"

# دستور شروع
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! 👋\nمن دانیال هستم، ربات هوش مصنوعی تو!\nهر سوالی بپرس جواب میدم! 🤖")

# پاسخ به همه پیام‌ها
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        print(f"Received: {message.text}")
        reply = smart_reply(message.text)
        bot.reply_to(message, reply)
        print(f"Replied: {reply[:100]}")
    except Exception as e:
        print(f"Error: {str(e)}")
        bot.reply_to(message, "🤖 ممنون از پیامت! من هنوز در حال یادگیری هستم.")

print("🤖 Bot is running...")
bot.infinity_polling()
