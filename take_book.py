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


def take_book_user(update: Update, context: Any):
    "take information from db and make object of Book class"
    update.message.reply_text('Напишите название книги')
    # if not User.check_registration():  # обязательная проверка на зарегестрированность
    #     User.registration_func(update, context)
    # message = update.message.text
    # book = Book(User.find_book(message))


def take_book_1_user(update: Update, context: Any):
    value = update.message.text
    update.message.reply_text('\n'.join(get_items('url', 'Books', 'title', value)))
