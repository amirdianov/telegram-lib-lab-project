import logging
import sqlite3
import time
from typing import Any

from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, \
    CallbackContext, PrefixHandler
from db_func import add_item


def check_registration():
    """u can make this method not static, how u can - make"""
    # if user in data_base:
    #     return True
    # else:
    #     return False
    return False

#def registration_user(self: Update, context: Any):
def begin_registration_user(self: Update, context: Any):
    """make people to registred and insert to db"""
    """use ConversationHandler to insert user for db"""
    if check_registration():
        self.message.reply_text('Вы уже зарегистрированы в системе👍')
        return ConversationHandler.END
    else:
        self.message.reply_text('Давайте регистрироваться. Введите свои данные')
        return 1

def handle_user_data(self: Update, context: Any):
    """handle user data and insert it into db"""
    context.user_data['name_surname']: str = update.message.text.strip()
    update_items('users', 'name_surname', 'telegram_id', context.user_data['name_surname'], self.message.from_user.id)
    self.message.reply_text('Вы успешно зарегистровались ✅')
    return ConversationHandler.END

