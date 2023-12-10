# -*- coding: utf-8 -*-
import telebot
import random
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

states = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    reg = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
    markup.add(reg)

    bot.send_message(message.chat.id, "Привет! Этот бот разработан специально для РПО 23/1 и его целью является определение получателя для тайного санты", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Еще раз тебя приветствую, мой дорогой друг, вижу вам нужна помощь.\nПуть к определению человека,которому тебе нужно готовить подарок: \n1.Написать команду /start либо выбрать в нижнем меню\n2.Под тем сообщением будет кнопка зарегистрироваться, ее нужно нажать\n3.Введит свою фамилию в именительном падеже с заглавной буквы\n4.Начинайте готовить подарок тому человеку)")

@bot.callback_query_handler(lambda call: True)
def callback(call):
    if call.message:
        if call.data == "reg":
            bot.send_message(call.message.chat.id, 'Напишите свою фамилию в именительном падеже с заглавной буквы')
            states[call.message.chat.id] = 'reg'

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    user_message = message.text

    name_list = [
        "Кольцов", "Бурыкин", "Висков", "Дворова", "Муравьев", "Подлесняк", "Коршунов",
        "Данилов", "Хрыкин", "Винидиктова", "Колтун", "Аверьянов", "Рустамов", "Чиботарь",
        "Булычев", "Стребков", "Оськин", "Фатехов", "Усов"
    ]

    if message.chat.id in states and states[message.chat.id] == 'reg':
        states[message.chat.id] = None
        if user_message in name_list:
            name_list.remove(user_message)
            random_element = random.choice(name_list)
            bot.send_message(message.chat.id, f"Вам нужно подготовить подарок для: {random_element}")
        else:
            bot.send_message(message.chat.id, "Вашей фамилии нет в списке. Пожалуйста, попробуйте еще раз")
    else:
        photo = open('фото.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Я не понял ваш запрос")


try:
    bot.polling(non_stop=True)
except Exception as e:
    print(f"Произошло исключение: {e}") #Такие исключения нужны были? я не поняла Т.Т
