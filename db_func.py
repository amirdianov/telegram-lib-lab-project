import logging
import sqlite3
import time
from typing import Any

from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, \
    CallbackContext, PrefixHandler

'''some functions to work with db'''
conn = sqlite3.connect('library.sqlite', check_same_thread=False)
cursor = conn.cursor()


# doesn't work now
def add_item(self, item_text, owner):
    stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
    args = (item_text, owner)
    cursor.execute(stmt, args)
    conn.commit()


# doesn't work now
def delete_item(self, item_text, owner):
    stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
    args = (item_text, owner)
    cursor.execute(stmt, args)
    conn.commit()


# work
# url = [x[0] for x in cursor.execute('SELECT url from Books WHERE title = (?)', (book,))]
def get_items(from_which_column, table, column_where, value):
    stmt = f'SELECT {from_which_column} FROM {table} WHERE {column_where} = (?)'
    args = (value,)
    return [x[0] for x in cursor.execute(stmt, args)]


# doesn't work now
def update_items():
    pass
