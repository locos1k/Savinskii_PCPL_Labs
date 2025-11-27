import telebot
from telebot import types
import random

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

duels = {}
stats = {}
rpg_stats = {}
rpg_battles = {}  

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🎲 Бросить кубик")
    btn2 = types.KeyboardButton("🔢 Случайное число")
    btn3 = types.KeyboardButton("🪙 Монета")
    btn4 = types.KeyboardButton("❓ Помощь")
    btn5 = types.KeyboardButton("📊 Статистика")
    btn6 = types.KeyboardButton("🗡 RPG-атака")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

    bot.send_message(
        message.chat.id,
        "Привет! Я RandomGameBot. Выбери действие 👇",
        reply_markup=markup
    )

@bot.message_handler(commands=['duel'])
def duel_command(message):
    chat_id = message.chat.id
    chat_type = message.chat.type

    if chat_type == "private":
        bot.send_message(chat_id, "Дуэли доступны только в групповых чатах 🙂")
        return

    challenger = message.from_user
    opponent = None

    if message.reply_to_message:
        opponent = message.reply_to_message.from_user

    if not opponent and message.entities:
        for ent in message.entities:
            if ent.type == "text_mention" and ent.user:
                opponent = ent.user
                break

            if ent.type == "mention":
                username = message.text[ent.offset: ent.offset + ent.length] 
                try:
                    chat = bot.get_chat(username)
                    opponent = chat
                    break
                except Exception:
                    pass

    if not opponent:
        bot.send_message(
            chat_id,
            "Чтобы начать дуэль, ответь на сообщение соперника командой /duel\n"
            "или напиши /duel и выбери его через упоминание."
        )
        return

    if challenger.id == opponent.id:
        bot.send_message(chat_id, "Нельзя вызвать на дуэль самого себя)")
        return
    
    if opponent.is_bot:
        bot.send_message(chat_id, "Нельзя вызвать меня на дуэль!")
        return

    duels[chat_id] = {
        "challenger_id": challenger.id,
        "opponent_id": opponent.id,
        "challenger_name": challenger.first_name or "Игрок 1",
        "opponent_name": opponent.first_name or "Игрок 2",
        "rolls": {}
    }

    bot.send_message(
        chat_id,
        f"⚔️ Дуэль!\n"
        f"{duels[chat_id]['challenger_name']} вызывает {duels[chat_id]['opponent_name']}.\n\n"
        f"Нажмите на кнопку «🎲 Бросить кубик»."
    )

@bot.message_handler(commands=['rpg'])
def rpg_command(message):
    chat_id = message.chat.id
    chat_type = message.chat.type

    if chat_type == "private":
        bot.send_message(chat_id, "RPG-сражения доступны только в групповых чатах 🙂")
        return

    challenger = message.from_user
    opponent = None

    if message.reply_to_message:
        opponent = message.reply_to_message.from_user

    if not opponent and message.entities:
        for ent in message.entities:
            if ent.type == "text_mention" and ent.user:
                opponent = ent.user
                break

            if ent.type == "mention":
                username = message.text[ent.offset: ent.offset + ent.length] 
                try:
                    chat = bot.get_chat(username) 
                    opponent = chat
                    break
                except Exception:
                    pass

    if not opponent:
        bot.send_message(
            chat_id,
            "Чтобы начать RPG-бой, ответь на сообщение соперника командой /rpg\n"
            "или напиши /rpg и выбери его через упоминание."
        )
        return

    if challenger.id == opponent.id:
        bot.send_message(chat_id, "Нельзя сражаться с самим собой")
        return
    
    if opponent.is_bot:
        bot.send_message(chat_id, "Нельзя вызвать меня на RPG-бой!")
        return

    if chat_id in rpg_battles:
        bot.send_message(chat_id, "В этом чате уже идёт RPG-бой! Сначала завершите его.")
        return

    hp_start = 30
    rpg_battles[chat_id] = {
        "p1_id": challenger.id,
        "p2_id": opponent.id,
        "p1_name": challenger.first_name or "Игрок 1",
        "p2_name": opponent.first_name or "Игрок 2",
        "hp": {
            challenger.id: hp_start,
            opponent.id: hp_start,
        },
        "turn": challenger.id,
    }

    bot.send_message(
        chat_id,
        f"🗡 Начинается RPG-бой!\n"
        f"{rpg_battles[chat_id]['p1_name']} VS {rpg_battles[chat_id]['p2_name']}\n"
        f"У каждого по {hp_start} HP.\n\n"
        f"Ход {rpg_battles[chat_id]['p1_name']}. Нажмите кнопку «🗡 Атака»."
    )



@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text or ""
    chat_type = message.chat.type

    if text.startswith("/"):
        return

    if chat_type == "private":
        if text == "🎲 Бросить кубик":
            roll = random.randint(1, 6)

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

    elif chat_type in ("group", "supergroup"):
        chat_id = message.chat.id
        user_id = message.from_user.id
        name = message.from_user.first_name or "Игрок"

        if text == "🎲 Бросить кубик":
            roll = random.randint(1, 6)
            bot.send_message(chat_id, f"{name} бросил(а) кубик: {roll} 🎲")

            state = duels.get(chat_id)
            if state and user_id in (state["challenger_id"], state["opponent_id"]):
                if user_id in state["rolls"]:
                    return

                state["rolls"][user_id] = roll
                
                if len(state["rolls"]) == 2:
                    c_id = state["challenger_id"]
                    o_id = state["opponent_id"]
                    c_name = state["challenger_name"]
                    o_name = state["opponent_name"]
                    c_roll = state["rolls"][c_id]
                    o_roll = state["rolls"][o_id]

                    result_text = (
                        "⚔️ *Итоги дуэли:*\n\n"
                        f"{c_name}: {c_roll}\n"
                        f"{o_name}: {o_roll}\n\n"
                    )

                    if c_roll > o_roll:
                        winner_id = c_id
                        winner_name = c_name
                    elif o_roll > c_roll:
                        winner_id = o_id
                        winner_name = o_name
                    else:
                        winner_id = None

                    if winner_id is None:
                        result_text += "🤝 Ничья!"
                    else:
                        result_text += f"🏆 Победитель: *{winner_name}*!"

                        if winner_id not in stats:
                            stats[winner_id] = 0
                        stats[winner_id] += 1

                    bot.send_message(chat_id, result_text, parse_mode="Markdown")
                    duels.pop(chat_id, None)

        elif text == "🗡 RPG-атака":
            state = rpg_battles.get(chat_id)
            if not state:
                bot.send_message(chat_id, "Сначала начните RPG-бой командой /rpg (по реплаю или с упоминанием).")
                return

            if user_id not in (state["p1_id"], state["p2_id"]):
                bot.send_message(chat_id, "Ты не участвуешь в этом сражении.")
                return

            if state["turn"] != user_id:
                current_name = state["p1_name"] if state["turn"] == state["p1_id"] else state["p2_name"]
                bot.send_message(chat_id, f"Сейчас ход {current_name}!")
                return

            attacker_id = user_id
            defender_id = state["p2_id"] if attacker_id == state["p1_id"] else state["p1_id"]
            attacker_name = state["p1_name"] if attacker_id == state["p1_id"] else state["p2_name"]
            defender_name = state["p2_name"] if defender_id == state["p2_id"] else state["p1_name"]

            dmg = random.randint(5, 15)
            state["hp"][defender_id] -= dmg
            if state["hp"][defender_id] < 0:
                state["hp"][defender_id] = 0

            attacker_hp = state["hp"][attacker_id]
            defender_hp = state["hp"][defender_id]

            text_out = (
                f"🗡 {attacker_name} атакует {defender_name} и наносит {dmg} урона!\n"
                f"HP {attacker_name}: {attacker_hp}\n"
                f"HP {defender_name}: {defender_hp}\n"
            )

            if defender_hp <= 0:
                text_out += f"\n💀 {defender_name} пал в бою.\n🏆 Победитель: {attacker_name}!"

                winner_id = attacker_id
                if winner_id not in rpg_stats:
                    rpg_stats[winner_id] = 0
                rpg_stats[winner_id] += 1

                bot.send_message(chat_id, text_out)
                rpg_battles.pop(chat_id, None)
            else:
                state["turn"] = defender_id
                text_out += f"\nТеперь ход {defender_name} (нажми «🗡 RPG-атака»)."
                bot.send_message(chat_id, text_out)

        elif text == "❓ Помощь":
            bot.send_message(
                chat_id,
                "Это групповой режим.\n"
                "⚔️ Дуэль 1х1:\n"
                "   • Ответь на сообщение соперника командой /duel\n"
                "   • Оба жмите «🎲 Бросить кубик».\n\n"
                "🗡 RPG-бой:\n"
                "   • Ответь на сообщение соперника командой /rpg\n"
                "   • Или используй /rpg с упоминанием.\n"
                "   • Затем по очереди жмите «🗡 RPG-атака», пока у кого-то не кончится HP."
            )
        
        elif text == "🔢 Случайное число":
            bot.send_message(message.chat.id, f"Случайное число: {random.randint(1, 100)} 🔢")

        elif text == "🪙 Монета":
            bot.send_message(message.chat.id, f"Монета: {random.choice(['орёл', 'решка'])}")

        elif text == "📊 Статистика":
            user_id = message.from_user.id
            duel_wins = stats.get(user_id, 0)
            rpg_wins = rpg_stats.get(user_id, 0)
            bot.send_message(
                chat_id,
                f"📊 Ваша статистика:\n"
                f"• Побед в дуэлях: {duel_wins}\n"
                f"• Побед в RPG-боях: {rpg_wins}"
            )
        else:
            return

bot.infinity_polling()