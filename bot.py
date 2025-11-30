import telebot
from telebot import types

bot = telebot.TeleBot("7671560262:AAEGBuDLb_nqLh07CWmDbTebNQTISMkUv4g")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📖 Притча о Забвении")
    btn2 = types.KeyboardButton("🌐 Все притчи")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id,
        "🎇 *Добро пожаловать в мир духовных притч!*\n\n"
        "Я - @ParablesBot, хранитель мудрости.\n"
        "Выбери притчу или воспользуйся командами:\n"
        "/list - все притчи\n"
        "/site - библиотека онлайн",
        parse_mode='Markdown',
        reply_markup=markup)

@bot.message_handler(commands=['list'])
def list_parables(message):
    text = """
📚 *Доступные притчи:*

1. Притча о Забвении
2. Скоро появятся новые...

🔮 *В разработке:*
- Притча об Образо-вании
- Притча о Трехритмичном Дыхании
- Притча о Сфере Эго
    """
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['site'])
def site(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🌐 Открыть библиотеку", 
                                   url="https://breathingmusic.netlify.app/")
    markup.add(btn)
    
    bot.send_message(message.chat.id,
        "📖 *Онлайн-библиотека притч:*",
        reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "📖 Притча о Забвении":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📖 Читать притчу", 
                                       url="https://valswift.github.io/static-website/parable2.html")
        markup.add(btn)
        
        bot.send_message(message.chat.id,
            "📖 *Притча о Забвении*\n\n"
            "Откровение о божественном происхождении Эго "
            "и смысле творения.\n\n"
            "#Притча #Осознанность #СВА",
            parse_mode='Markdown',
            reply_markup=markup)
    
    elif message.text == "🌐 Все притчи":
        site(message)

if __name__ == "__main__":
    print("Бот @ParablesBot запущен!")
    bot.polling(none_stop=True)