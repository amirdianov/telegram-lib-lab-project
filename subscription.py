import datetime
import logging
import sqlite3
import time
import datetime
import calendar
from typing import Any

from telegram import Update, ForceReply, ReplyKeyboardMarkup, LabeledPrice, ShippingOption
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CommandHandler, Filters, \
    CallbackContext, PrefixHandler
from db_func import get_items, update_items

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


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def new_dates_user(self: Update, context: Any, user_id):
    somedate = datetime.date.today()
    # date_start = somedate
    # date_finish = add_months(date_start, 1)
    date_start = datetime.datetime.strftime(somedate, "%Y.%m.%d")
    date_finish = datetime.datetime.strftime(add_months(somedate, 1), "%Y.%m.%d")

    update_items('Subscription', 'exists_since', 'telegram_id', date_start, user_id)
    update_items('Subscription', 'valid_until', 'telegram_id', date_finish, user_id)
    update_items('Users', 'subscription', 'telegram_id', True, user_id)
    update_items('Subscription', 'activity', 'telegram_id', True, user_id)


def subscription_user(self: Update, context: Any):
    "take information from db and make object of Subscription class"
    user_id = self.message.from_user.id
    if not check_registration(user_id):  # обязательная проверка на зарегистрированность
        self.message.reply_text('❌ К сожалению, вы не зарегистрированы в нашей системе ❌ \n'
                                'Пройдите регистрацию для возможности взятия книги 💻')
        return False
    else:
        return True


def subscription_activated_check(self: Update, context: Any):
    user_id = self.message.from_user.id
    if not activated_subscription(user_id):
        self.message.reply_text('❌ К сожалению, ваша подписка не активна ❌ \n'
                                'Для этого нужно оформить подписку. Хотите это сделать? 📅')
        return False
    else:
        return True


def subscription_need_active(self: Update, context: Any):
    methods_reply_keyboard = [['Да, давайте оформим!', 'Нет, спасибо.'], ['📃methods']]
    methods_markup = ReplyKeyboardMarkup(methods_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    self.message.reply_text('Решайте!', reply_markup=methods_markup)


def subscription_need_ans(self: Update, context: Any):
    ans = self.message.text
    if ans == 'Да, давайте оформим!':
        start_without_shipping_callback(self, context)
        self.message.reply_text('Мы ожидаем вашей оплаты!')
        return True
    elif ans == 'Нет, спасибо.':
        self.message.reply_text('Очень жаль. Тогда вдругой раз!')
        return False
    elif ans == '📃methods':
        return False


# don't touch this, but u can use it
def start_without_shipping_callback(update: Update, context: CallbackContext) -> None:
    """Sends an invoice without shipping-payment."""
    chat_id = update.message.chat_id
    title = "Оплата подписки"
    description = "Оплата подписки с целью получения доступа ко всем книгам LibLab"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    provider_token = "1744374395:TEST:737379f130b29ee8ceb3"
    currency = "RUB"
    # price in dollars
    price = 299
    # price * 100 so as to include 2 decimal points
    prices = [LabeledPrice("Test", price * 100)]
    photo_url = 'https://thumbs.gfycat.com/AgonizingAggravatingCattle-size_restricted.gif'
    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    context.bot.send_invoice(
        chat_id, title, description, payload, provider_token, currency,
        prices, photo_url=photo_url, photo_width=900, photo_height=600
    )
