




import logging
import sqlite3
import time
from typing import Any

from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, \
    CallbackContext, PrefixHandler
from db_func import get_items

from registration import check_registration


def activated_subscription(user_id):
    """use db, u can make this method not static, how u can - make"""
    if get_items('activity', 'subscription', 'telegram_id', user_id)[0] == 1:
        return True
    else:
        return False


def renew_dates_user(self: Update, context: CallbackContext):
    """methods renew dates of subscription, if its ended"""
    return True


def subscription_user(self: Update, context: Any):
    "take information from db and make object of Subscription class"
    user_id = self.message.from_user.id
    if not check_registration(user_id):  # обязательная проверка на зарегистрированность
        self.message.reply_text('❌ К сожалению, вы не зарегистрированы в нашей системе ❌ \n'
                                'Пройдите регистрацию для возможности взятия книги 💻')
        return False
    else:
        if activated_subscription(user_id):
            # ветка наличия подписки
            ...
        else:
            # ветка отсутствия подписки
            # дописать функцию
            ...
    # subscription = Subscription(User.find_subscription())
    self.message.reply_text('Ваша подписка активна или не активна - вопрос')
