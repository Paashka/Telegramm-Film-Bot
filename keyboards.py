import telebot
from config import TYPES

def get_main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('➕ Добавить', '📋 Список')
    markup.row('❌ Удалить')
    return markup

def get_types_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item_type in TYPES:
        markup.row(item_type)
    return markup