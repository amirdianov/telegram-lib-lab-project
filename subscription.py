import logging
import sqlite3
import time
from typing import Any

from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, \
    CallbackContext, PrefixHandler

from registration import check_registration


def find_subscription():
    """use db, u can make this method not static, how u can - make"""
    return True


def renew_dates_user(self: Update, context: CallbackContext):
    """methods renew dates of subscription, if its ended"""
    return True


def subscription_user(self: Update, context: Any):
    "take information from db and make object of Subscription class"
    if not check_registration():  # обязательная проверка на зарегестрированность
        check_registration()
    # subscription = Subscription(User.find_subscription())
    self.message.reply_text('Ваша подпска активна или не активна - вопрос')
