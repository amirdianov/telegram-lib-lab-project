"""
Telegram bot LibLab
"""

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN: str = '5224259246:AAGQVvCAIGbuk2YxeQcPFxpNzCNQ4E46qM4'

def start_messaging(update: Updater, context: CallbackContext) -> int:
    """Function greets the user"""
    update.message.reply_text('Вас приветствует телеграм-бот электронной библиотеки LibLab👋'
            'В нашей библиотеке представлена внушительная коллекция книг на любой вкус👍'
            'Желаю вам приятного чтения🤓')


def main() -> None:
    """main function organizes work of our bot"""
    updater: Updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_messaging))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()