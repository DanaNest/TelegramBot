import telebot
from extensions import APIException, CurrencyConvert
from config import currency, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}\n \
введите /help, чтобы узнать как работать с ботом")


@bot.message_handler(commands=['help'])
def begin(message: telebot.types.Message):
    text = 'Чтобы начать работу введите в \
следующем формате:\n<имя валюты, цену которой хотите узнать>\n\
<имя валюты, в которой надо узнать цену первой>\n\
<количество первой валюты> через пробел прописными буквами.\nУвидеть список всех \
доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Валюты для перевода:'
    for cur in currency:
        text = '\n'.join((text, cur, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        quote, base, amount = values

        total_base = CurrencyConvert.get_price(quote, base,amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить. \n{e}')
    else:
        price = total_base.get('conversion_result')
        price = round(price, 2)
        text = f'Цена {amount} {quote} в {base} - {price}'
        bot.send_message(message.chat.id, text)


bot.polling()



