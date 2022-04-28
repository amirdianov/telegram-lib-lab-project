import logging
import re
import sqlite3
import time
from typing import Any

from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, \
    CallbackContext, PrefixHandler
from db_func import add_item, update_items, get_items


def check_registration(user_id: int) -> bool:
    """u can make this method not static, how u can - make"""
    ans = get_items('registration', 'Users', 'telegram_id', user_id)[0]
    if ans != 0:
        return True
    return False


def begin_registration_user(update: Update, context: Any):
    """make people to registred and insert to db"""
    """use ConversationHandler to insert user for db"""
    if check_registration(update.message.from_user.id):
        update.message.reply_text('Вы уже зарегистрированы в системе👍')
        return False
    else:
        update.message.reply_text('Давайте регистрироваться 📝.\nВведите свои фамилию и имя через пробел.\n'
                                  'Допустимые символы: заглавные и строчные буквы кириллицы и пробел.\n'
                                  'Например, Иванов Иван.😉')
        return True


def registration_handle_user_data(update: Update, context: Any):
    """handle user data and insert it into db"""
    context.user_data['name_surname']: str = update.message.text.strip().title()
    re_expression: str = re.search(r'[А-Яа-я]+ +[А-Яа-я]+', context.user_data['name_surname'])
    if re_expression is None or re_expression.group() != \
            context.user_data['name_surname']:
        update.message.reply_text('Фамилия и имя введены неправильно ⛔️😪\n'
                                  '🔄 Давай попробуем ввести их заново, но сначала я напомню основные правила ввода:\n'
                                  'Допустимые символы: заглавные и строчные буквы кириллицы и пробел.\n'
                                  'Например, Иванов Иван.😉')
        return False
    fullname: str = context.user_data['name_surname']
    fullname = fullname[:fullname.find(' ')] + \
               fullname[fullname.rfind(' '):]
    context.user_data['name_surname'] = fullname
    update_items('users', 'name_surname', 'telegram_id', context.user_data['name_surname'],
                 update.message.from_user.id)
    update_items('users', 'registration', 'telegram_id', True,
                 update.message.from_user.id)
    update.message.reply_text('✅ Регистрация прошла успешно.\n'
                              f'{context.user_data["name_surname"]}, добро пожаловать '
                              f'в сообщество нашей библиотеки! 🎆')
    return True
