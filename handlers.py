import telebot
from database import Database
from keyboards import get_main_keyboard, get_types_keyboard
from config import TYPES

db = Database()


def register_handlers(bot): #обработчик

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        text = """
Привет! Я помогу разобраться с фильмами и сериалами.

Вот что я умею:
1) Добавить фильм/сериал в общий список
2) Посмотреть что уже добавлено
3) Удалить любой фильм

        """
        bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard())

    @bot.message_handler(func=lambda message: message.text == '➕ Добавить')
    def add_item_start(message):
        msg = bot.send_message(message.chat.id, 'Напиши название фильма или сериала:') #добавление
        bot.register_next_step_handler(msg, process_add_name)

    def process_add_name(message):
        if not message.text: #проверка названия
            bot.send_message(message.chat.id, 'Название не может быть пустым!')
            return

        user_data = {
            'name': message.text
        }

        msg = bot.send_message(message.chat.id,
                               f'Название: {message.text}\n\nВыбери категорию:',
                               reply_markup=get_types_keyboard())
        bot.register_next_step_handler(msg, process_add_type, user_data)

    def process_add_type(message, user_data): #обработка по запросу
        if message.text not in TYPES:
            bot.send_message(message.chat.id, 'Выбери из кнопок!')
            return

        item = db.add_item(user_data['name'], message.text) #сохранениие в watchlist

        text = f"""
✅ Добавлено в общий список:

{message.text} - {user_data['name']}
📅 {item['date']}
📝 ID: {item['id']}

        """

        bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard())

    @bot.message_handler(func=lambda message: message.text == '📋 Список')
    def show_list(message):
        items = db.get_all_items()  #получаем все записи

        if not items:
            bot.send_message(message.chat.id, 'Список пуст!')
            return

        text = '🎬 Список фильмов:\n\n'

        for i, item in enumerate(items, 1):
            text += f'{i}. {item['type']} - {item['name']}\n'
            text += f"   📅 {item['date']}\n\n"

        if len(text) > 4000: #если список очень длинный, показываем последние 20
            items = db.get_last_items(20)
            text = '🎬 Последние 20 фильмов:\n\n'
            for i, item in enumerate(items, 1):
                text += f'{i}. {item['type']} - {item['name']}\n'
                text += f'   📅 {item['date']}\n\n'

        bot.send_message(message.chat.id, text)

    @bot.message_handler(func=lambda message: message.text == '❌ Удалить')
    def delete_start(message): #запрос на удаление
        items = db.get_all_items()

        if not items: #првоерка списка
            bot.send_message(message.chat.id, 'Список пуст')
            return

        text = '❌ Удалить из общего списка:\n\n'
        text += 'Введи номер фильма для удаления\n'

        last_items = db.get_last_items(10) #недавно добавленные 10
        text += 'Последние добавленные:\n'
        for item in last_items:
            text += f'{item['id']}: {item['name']}\n'

        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, process_delete)

    def process_delete(message): #функ удаления по ID
        try:
            item_id = int(message.text)
            items = db.get_all_items()

            #ID = фильм
            found_item = None
            for item in items:
                if item['id'] == item_id:
                    found_item = item
                    break

            if not found_item:
                bot.send_message(message.chat.id, f'Фильм с ID {item_id} не найден')
                return

            if db.delete_item(item_id):
                bot.send_message(message.chat.id, f"✅ Фильм '{found_item['name']}' удален")
            else:
                bot.send_message(message.chat.id, 'Ошибка при удалении')

        except ValueError:
            bot.send_message(message.chat.id, 'Введи число')

    @bot.message_handler(func=lambda message: True)
    def handle_other(message):
        if message.text:
            bot.send_message(message.chat.id,
                             'Используй кнопки внизу',
                             reply_markup=get_main_keyboard())