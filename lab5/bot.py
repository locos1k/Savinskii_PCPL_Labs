import telebot
from telebot import types
import random

TOKEN = "8540127884:AAFPVgs8B25AMIlTgvRWdUP0Bdc_0Y4hEXg"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🎲 Бросить кубик")
    btn2 = types.KeyboardButton("🔢 Случайное число")
    btn3 = types.KeyboardButton("🪙 Монета")
    btn4 = types.KeyboardButton("❓ Помощь")

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        "Привет! Я RandomGameBot. Выбери действие 👇",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text

    if text == "🎲 Бросить кубик":
        bot.send_message(message.chat.id, f"Выпало: {random.randint(1, 6)} 🎲")

    elif text == "🔢 Случайное число":
        bot.send_message(message.chat.id, f"Случайное число: {random.randint(1, 100)} 🔢")

    elif text == "🪙 Монета":
        bot.send_message(message.chat.id, f"Монета: {random.choice(['орёл', 'решка'])}")

    elif text == "❓ Помощь":
        bot.send_message(
            message.chat.id,
            "Что я умею:\n"
            "🎲 Бросить кубик\n"
            "🔢 Выдать случайное число\n"
            "🪙 Подбросить монету\n"
        )

    else:
        bot.send_message(message.chat.id, "Такой команды не найдено. Выберите действие по кнопке ниже")


bot.infinity_polling()