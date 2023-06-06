import telebot

TOKEN = "6244941191:AAGeu55-c5jZViifnNspE2TD71J35JgOIKA"
GROUP_ID = 952850510  # Замените на ID вашей группы

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start"""
    bot.send_message(chat_id=message.chat.id, text="Привет! Я бот для добавления участников в группу.")

@bot.message_handler(commands=['addmember'])
def add_member(message):
    """Обработчик команды /addmember"""
    user_id = message.from_user.id
    chat_id = GROUP_ID  # Используем заранее заданный ID группы

    # Добавляем пользователя в группу
    try:
        bot.add_chat_member(chat_id=chat_id, user_id=user_id)
        bot.send_message(chat_id=chat_id, text="Пользователь успешно добавлен в группу.")
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"Не удалось добавить пользователя в группу: {str(e)}")

@bot.message_handler(commands=['checkprivacy'])
def check_privacy(message):
    """Обработчик команды /checkprivacy"""
    chat_id = message.chat.id

    # Получаем информацию о чате
    chat = bot.get_chat(chat_id)

    report = "Пользователи с настройкой конфиденциальности, запрещающей добавление в группы:\n"

    # Получаем общее количество участников группы
    total_members = bot.get_chat_members_count(chat_id)

    # Перебираем идентификаторы участников и получаем информацию о каждом участнике
    for user_id in range(total_members):
        try:
            # Получаем информацию о пользователе
            member = bot.get_chat_member(chat_id=chat_id, user_id=user_id)

            if member.user.is_bot:
                continue

            # Проверяем настройки конфиденциальности участника
            if member.can_invite_users is False:
                report += f"Имя пользователя: {member.user.username} (ID: {member.user.id})\n"
        except Exception as e:
            print(f"Ошибка при получении информации о пользователе: {str(e)}")

    # Отправляем отчет в чат группы
    bot.send_message(chat_id=chat_id, text=report)

# Запускаем бота
bot.polling()