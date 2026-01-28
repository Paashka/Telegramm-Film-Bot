import telebot
from config import TOKEN
from handlers import register_handlers

def main():
    bot = telebot.TeleBot(TOKEN)

    register_handlers(bot)

    print("Бот запущен")

    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()