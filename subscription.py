import logging
import sqlite3
import time
from typing import Any

from telegram import Update, ForceReply, ReplyKeyboardMarkup, LabeledPrice, ShippingOption
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
        if not activated_subscription(user_id):
            # ветка отсутствия подписки
            return True
        else:
            # ветка наличия подписки
            # дописать функцию Алмазу
            # использовать renew_dates_user для обновления подписки
            return False


def start_without_shipping_callback(update: Update, context: CallbackContext) -> None:
    """Sends an invoice without shipping-payment."""
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    provider_token = "1744374395:TEST:737379f130b29ee8ceb3"
    currency = "RUB"
    # price in dollars
    price = 299
    # price * 100 so as to include 2 decimal points
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    context.bot.send_invoice(
        chat_id, title, description, payload, provider_token, currency, prices
    )


def shipping_callback(update: Update, context: CallbackContext) -> None:
    """Answers the ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
        return

    # First option has a single LabeledPrice
    options = [ShippingOption('1', 'Shipping Option A', [LabeledPrice('A', 100)])]
    # second option has an array of LabeledPrice objects
    price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
    options.append(ShippingOption('2', 'Shipping Option B', price_list))
    query.answer(ok=True, shipping_options=options)
