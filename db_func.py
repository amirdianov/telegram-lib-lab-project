import logging
import sqlite3
import time
from typing import Any
from itertools import chain

from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, \
    CallbackContext, PrefixHandler

'''some functions to work with db'''
conn = sqlite3.connect('library.sqlite', check_same_thread=False, timeout=1)
cursor = conn.cursor()


# work
# you don't need to touch this method
def add_item(user_id):
    cursor.execute("INSERT INTO Users (telegram_id, name_surname,subscription,registration) VALUES (?,?,?,?)",
                   (user_id, None, False, False))
    cursor.execute("INSERT INTO subscription (telegram_id, valid_until,  exists_since, activity) VALUES (?,?,?,?)",
                   (user_id, None, None, False))
    conn.commit()


# work
# url = [x[0] for x in cursor.execute('SELECT url from Books WHERE title = (?)', (book,))]
def get_items(from_which_column, table, column_where, value):
    '''return list values with value'''
    stmt = f'SELECT {from_which_column} FROM {table} WHERE {column_where} = (?)'
    args = (value,)
    return [x[0] for x in cursor.execute(stmt, args)]


# work
# cursor.execute('UPDATE Persons SET user_register = ? WHERE user_id = ?', (us_adress, us_id))
def update_items(table, what_past, where_past, value_past, where_value):
    cursor.execute(f'UPDATE {table} SET {what_past} = ? WHERE {where_past} = ?', (value_past, where_value))
    conn.commit()


def get_item(column: str, db_name: str, some_column: str, value: Any):
    cursor.execute(f"SELECT {column} FROM {db_name} WHERE {some_column} = '{value}'")
    return cursor.fetchall()


def get_all_value_from_column(column: str):
    cursor.execute(f"SELECT {column} FROM Books")
    return cursor.fetchall()


def main_get_item(db_name: str, some_column: str, value: Any, *args, **kwargs):
    selected_columns = ','.join(chain(args, kwargs.values()))
    cursor.execute(f"SELECT {selected_columns} FROM {db_name} WHERE {some_column} = '{value}'")
    return cursor.fetchall()
