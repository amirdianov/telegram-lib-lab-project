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


def registration_user(self: Update, context: Any):
    """make people to registred and insert to db"""
    """use ConversationHandler to insert user for db"""
    self.message.reply_text('Давайте регестрироваться. Введите свои данные')
