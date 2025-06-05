import telebot
from bot_logic import gen_pass, gen_emodji, flip_coin  
from my_model import detect_deapfake_or_real_person

bot = telebot.TeleBot('8119500631:AAHDitnnXOQOw--jbpbgLmS4bOx_SK7LN9E')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """Привет! Я твой Telegram бот.
                  Напиши команду /hello, /bye, /pass, /emodji , /photo или /coin""")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def send_password(message):
    password = gen_pass(10)  
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.reply_to(message, f"Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        file_name = file_info.file_path.split('/')[-1]
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Фото получено. Анализирую...")
        result = detect_deapfake_or_real_person(file_name)
        bot.reply_to(message, result)

    except Exception:
        bot.reply_to(message, f"Произошла ошибка при обработке изображения: {str(Exception)}")

bot.polling()