import logging
import sqlite3
import time
from typing import Any

from telegram import Update, ForceReply, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, \
    CallbackContext, PrefixHandler

from registration import check_registration
from db_func import *
from subscription import activated_subscription


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

def inner_find_book_function(user: Update, context: Any, canon: str):
    user.message.reply_text(f'📚Введите {canon} книги:')

def inner_take_book(self: Update, context: Any, user_message: str, criterion: str):
    user_id = self.message.from_user.id
    is_subscriber = activated_subscription(user_id)
    needed_books = main_get_item(db_name='Books', some_column=criterion, value=user_message,
    column1='title', column2='name', column3='subscription_need')
    def smile(status):
        return '🔒' if status else '✅'
    buttons_list: list[list[str]] = []
    urls_list = main_get_item(column1='url', db_name='Books', some_column=criterion, value=user_message)
    for index, book_name in enumerate(needed_books):
        kw_args = {}
        if is_subscriber or not book_name[2]:
            kw_args['url'] = urls_list[index][0][:-1]
        else:
            kw_args['callback_data'] = 'need_to_get_subscription'
        button = InlineKeyboardButton(text=smile(book_name[2]) + book_name[0] + ' ' + book_name[1], **kw_args)
        buttons_list.append([button])
    print(buttons_list)
    reply_markup_books = InlineKeyboardMarkup(buttons_list, one_time_keyboard=True, resize_keyboard=True)
    self.message.reply_text('📋Список книг, удовлетворяющих выбранным критериям:',
                            reply_markup=reply_markup_books if len(buttons_list) else ReplyKeyboardMarkup([['📖take_book']]))
    self.message.reply_text('Если хотите перейти в основное меню, нажмите на кнопку внизу ⬇⬇', reply_markup=
    ReplyKeyboardMarkup([['/methods']], resize_keyboard=True))

def take_book_1_user(self: Update, context: Any):
    value = self.message.text
    self.message.reply_text('\n'.join(get_items('url', 'Books', 'title', value)))
