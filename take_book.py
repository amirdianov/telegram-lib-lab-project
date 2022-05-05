import logging
import sqlite3
import time
from typing import Any

from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, \
    CallbackContext, PrefixHandler

from registration import check_registration
from db_func import *


def find_book(book):
    """use db"""
    return True


def take_book_user(self: Update, context: Any):
    "checking user in db"
    user_id = self.message.from_user.id
    if check_registration(user_id):
        return True
    else:
        self.message.reply_text('Пройдите регистрацию💻')
        return False


def take_book_type(self: Update, context: Any):
    reply_keyboard = [['title', 'genre'], ['author', 'rating']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    self.message.reply_text('По какому критерию книги показать?', reply_markup=markup)


def take_book_1_user(self: Update, context: Any):
    value = self.message.text
    self.message.reply_text('\n'.join(get_items('url', 'Books', 'title', value)))
