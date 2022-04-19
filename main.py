"""
Telegram bot LibLab
"""

import logging

from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN: str = '5224259246:AAGQVvCAIGbuk2YxeQcPFxpNzCNQ4E46qM4'

methods_reply_keyboard = [['/take_book', '/subscription'], ['/help', '/registration']]
methods_markup = ReplyKeyboardMarkup(methods_reply_keyboard, one_time_keyboard=True)


def start_messaging(update: Update, context: CallbackContext) -> int:
    """Function greets the user"""
    update.message.reply_text('Вас приветствует телеграм-бот электронной библиотеки LibLab 👋\n'
            'В нашей библиотеке представлена внушительная коллекция книг на любой вкус 👍\n'
            'Желаю вам приятного чтения 🤓')
    methods(update, context)


def take_book():
    pass


def subscription():
    pass


def help():
    pass


def registration():
    pass


def methods(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Вот действующие методы:', reply_markup=methods_markup)


def main() -> None:
    """main function organizes work of our bot"""
    updater: Updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_messaging))
    dispatcher.add_handler(CommandHandler('take_book', take_book))
    dispatcher.add_handler(CommandHandler('subscription', subscription))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('registration', registration))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
