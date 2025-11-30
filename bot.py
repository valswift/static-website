import os
import telebot
from telebot import types
from flask import Flask, request
import threading
import time

# Используем переменную окружения для безопасности токена
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7671560262:AAEGBuDLb_nqLh07CWmDbTebNQTISMkUv4g')

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Список притч для легкого управления
PARABLES = {
    "забвение": {
        "title": "📖 Притча о Забвении",
        "url": "https://valswift.github.io/static-website/parable2.html",
        "description": "Откровение о божественном происхождении Эго и смысле творения."
    },
    "зеркала": {
        "title": "🔮 Притча о Зеркалах Восприятия", 
        "url": "https://valswift.github.io/static-website/parable.html",
        "description": "О природе видения и осознанности дыхания."
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("📖 Притча о Забвении")
    btn2 = types.KeyboardButton("🔮 Притча о Зеркалах")
    btn3 = types.KeyboardButton("🌐 Все притчи")
    btn4 = types.KeyboardButton("📚 Библиотека")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(
        message.chat.id,
        "🎇 *Добро пожаловать в мир духовных притч!*\n\n"
        "Я - @ParablesBot, хранитель мудрости.\n"
        "Выбери притчу или воспользуйся командами:\n"
        "/list - все притчи\n"
        "/site - библиотека онлайн\n"
        "/help - справка",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
*Доступные команды:*

/start - начать работу
/list - список всех притч  
/site - онлайн библиотека
/help - эта справка

*Хештеги:*
#Притча #Осознанность #СВА #Дыхание #Эго
"""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['list'])
def list_parables(message):
    text = "📚 *Доступные притчи:*\n\n"
    for key, parable in PARABLES.items():
        text += f"• {parable['title']}\n"
    
    text += "\n🔮 *В разработке:*\n"
    text += "- Притча об Образо-вании\n"
    text += "- Притча о Трехритмичном Дыхании\n"
    text += "- Притча о Сфере Эго"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['site'])
def site(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🌐 Открыть библиотеку", url="https://breathingmusic.netlify.app/")
    btn2 = types.InlineKeyboardButton("📖 GitHub притчи", url="https://valswift.github.io/static-website/")
    markup.add(btn1, btn2)
    
    bot.send_message(
        message.chat.id,
        "📖 *Онлайн-библиотека притч:*",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.strip().lower()

    if text == "📖 притча о забвении" or "забвение" in text:
        send_parable(message, "забвение")
    
    elif text == "🔮 притча о зеркалах" or "зеркал" in text:
        send_parable(message, "зеркала")
    
    elif text == "🌐 все притчи" or "все" in text:
        list_parables(message)
    
    elif text == "📚 библиотека" or "библиотека" in text:
        site(message)
    
    else:
        bot.send_message(
            message.chat.id,
            "Не понял запрос 🤔 Используйте кнопки или команды /help",
            parse_mode='Markdown'
        )

def send_parable(message, parable_key):
    if parable_key in PARABLES:
        parable = PARABLES[parable_key]
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📖 Читать притчу", url=parable['url'])
        markup.add(btn)
        
        bot.send_message(
            message.chat.id,
            f"{parable['title']}\n\n{parable['description']}\n\n#Притча #Осознанность #СВА",
            parse_mode='Markdown',
            reply_markup=markup
        )

# Веб-хук для некоторых хостингов
@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your-domain.com/' + BOT_TOKEN)
    return "Бот работает!", 200

# Функция для запуска polling (для хостингов без веб-хуков)
def run_polling():
    while True:
        try:
            print("Запуск бота...")
            bot.polling(none_stop=True, interval=1)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("Бот @ParablesBot запущен!")
    
    # Автоматическое определение режима работы
    if os.environ.get('WEBHOOK_MODE'):
        # Режим веб-хука для Heroku-like хостингов
        app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    else:
        # Режим polling для обычных хостингов
        run_polling()