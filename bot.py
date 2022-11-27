import telebot
from telebot import types # для указание типов

bot = telebot.TeleBot("5814687996:AAEnSS4k2bYlX2iwpEMPxtifQgSBQIRa2G8", parse_mode=None)
storage = {}

def init_storage(user_id):
  storage[user_id] = dict(first=None, znak=None)

def store_number(user_id, key, value):
  storage[user_id][key] = dict(value=value)

def get_number(user_id, key):
  return storage[user_id][key].get('value')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    btn2 = types.KeyboardButton("Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Поздороваться":
        bot.send_message(message.chat.id, text="Привет!")
    elif message.text == "Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как тебя зовут?")
        btn2 = types.KeyboardButton("Что ты можешь?")
        btn3 = types.KeyboardButton("Калькулятор")
        back = types.KeyboardButton("Вернуться")
        markup.add(btn1, btn2, back, btn3)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
        bot.register_next_step_handler
    elif message.text == "Как тебя зовут?":
        bot.send_message(message.chat.id, "Я просто бот")
    
    elif message.text == "Что ты можешь?":
        bot.send_message(message.chat.id, text="Поздороваться")
    
    elif message.text == "Калькулятор":
        init_storage(message.from_user.id)
        bot.send_message(message.chat.id, text="Введите первое число")
        bot.register_next_step_handler(message, calc1)

    elif message.text == "Вернуться":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Поздороваться")
        button2 = types.KeyboardButton("Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")

def calc1(message): 
    first = message.text
    try:
        x = int(first)
    except:
        bot.send_message(message.chat.id, text="Вы ввели не число")
        return 
    store_number(message.from_user.id, "first", first)
    bot.send_message(message.chat.id, text="Выберите операцию + - * /")
    bot.register_next_step_handler(message, znak)
    

def znak(message):
    znak = message.text
    if znak == "+" or znak == "-" or znak == "*" or znak == "/":
        store_number(message.from_user.id, "znak", znak)
    else:
        bot.send_message(message.chat.id, text="Вы ввели неверную операцию")
        return
    bot.send_message(message.chat.id, text="Введите второе число")
    bot.register_next_step_handler(message, calc)
    

def calc(message):
    second = message.text
    try:
        y = int(second)
    except:
        bot.send_message(message.chat.id, text="Вы ввели не число")
        return 
    x = int(get_number(message.from_user.id, "first"))
    z = get_number(message.from_user.id, "znak")
    if z == "+":
        xy = x + y
    elif z == "-":
        xy = x - y 
    elif z == "*":
        xy = x * y
    elif z == "/":
        xy = x / y
    bot.send_message(message.chat.id, text=xy)


bot.polling(none_stop=True)