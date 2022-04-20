"""
Telegram bot LibLab
"""

import logging
import time
from typing import Any

from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, \
    CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN: str = '5224259246:AAHb9K2K1QrWpwKgKnrm5ftXtcre3TcFbZw'


def command(update: Update, context: CallbackContext):
    # ['/take_book', '/subscription', '/help', '/registration']
    ending = ['📖', '📅', '❓', '💻']
    command = update.message.text
    # if command == '/start':
    #     start_messaging(update, context)
    if '/' + str(command)[:-1] == '/take_book' and command[-1] in ending:
        User.take_book(update, context)
    elif '/' + str(command)[:-1] == '/subscription' and command[-1] in ending:
        User.subscription(update, context)
    elif '/' + str(command)[:-1] == '/registration' and command[-1] in ending:
        User.registration(update, context)
    elif '/' + str(command)[:-1] == '/help' and command[-1] in ending:
        help_func(update, context)
    else:
        update.message.reply_text('Увы☹, но я тебя не понимаю.\nПопробуй воспользоваться этими командами👇')
        help_func(update, context)


def start_messaging(update: Update, context: CallbackContext) -> int:
    """Function greets the user"""
    update.message.reply_text('Вас приветствует телеграм-бот электронной библиотеки LibLab 👋\n'
                              'В нашей библиотеке представлена внушительная коллекция книг на любой вкус 👍\n'
                              'Желаю вам приятного чтения 🤓')
    methods_func(update, context)


def help_func(update: Update, context: CallbackContext) -> None:
    """Function gives some important information"""
    update.message.reply_text('Вам нужна помомщь❓ \nДавайте я вам расскажу о том, что я умею: \n'
                              'take_book📖 - этот метод позволяет пользователю получить книгу\n'
                              'subscription📅 - этот метод помогает пользователю оформить подписку\n'
                              'registration💻 - этот метод помогает пользователю зарегестрироваться в нашей библиотеке\n'
                              'Куда отправимся❓')
    time.sleep(2)
    methods_func(update, context)


def methods_func(update: Update, context: CallbackContext) -> None:
    """Function gets methods"""
    methods_reply_keyboard = [['take_book📖', 'subscription📅'], ['help❓', 'registration💻']]
    methods_markup = ReplyKeyboardMarkup(methods_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text('Вот действующие методы:', reply_markup=methods_markup)


class User:
    def __init__(self, id, name_surname, registration, subscription):
        self.id = id
        self.name_surname = name_surname
        self.registration = registration
        self.subscription = subscription

    @staticmethod
    def check_registration():
        """u can make this method not static, how u can - make"""
        # if user in data_base:
        #     return True
        # else:
        #     return False
        return True

    def registration(self: Update, context: Any):
        """make people to registred and insert to db"""
        """use ConversationHandler to insert user for db"""
        self.message.reply_text('Давайте регестрироваться')
        if User.check_registration():
            return True
        else:
            self.message.reply_text('Регистрация...')

    @staticmethod
    def find_subscription():
        """use db, u can make this method not static, how u can - make"""

    def subscription(self: Update, context: Any):
        "take information from db and make object of Subscription class"
        if not User.check_registration():  # обязательная проверка на зарегестрированность
            User.registration(self, context)
        # subscription = Subscription(User.find_subscription())
        self.message.reply_text('Ваша подпска активна или не активна - вопрос')

    @staticmethod
    def find_book(book):
        """use db, u can make this method not static, how u can - make"""
        return 0

    def take_book(update: Update, context: Any):
        "take information from db and make object of Book class"
        if not User.check_registration():  # обязательная проверка на зарегестрированность
            User.registration(update, context)
        message = update.message.text
        # book = Book(User.find_book(message))
        update.message.reply_text('У нас есть такая книга или увы ее нет')


class Subscription:
    def __init__(self, id, exists_since, valid_until, activity):
        self.id = id
        self.exists_since = exists_since
        self.valid_until = valid_until
        self.activity = activity

    def renew_dates(self, update: Update, context: CallbackContext):
        """methods renew dates of subscription, if its ended"""
        pass


class Book:
    def __init__(self, id, author, genre, availability):
        self.id = id
        self.author = author
        self.genre = genre
        self.availability = availability


def main() -> None:
    """main function organizes work of our bot"""
    updater: Updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_messaging))
    dispatcher.add_handler(MessageHandler(Filters.text, command, pass_user_data=True))
    dispatcher.add_handler(CommandHandler('methods', methods_func))
    dispatcher.add_handler(CommandHandler('help', help_func))
    dispatcher.add_handler(CommandHandler('take_book', User.take_book))
    dispatcher.add_handler(CommandHandler('subscription', User.subscription))
    dispatcher.add_handler(CommandHandler('registration', User.registration))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
