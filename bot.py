"""
Telegram bot LibLab
"""
import time

from telegram import ShippingOption, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import PreCheckoutQueryHandler, CallbackQueryHandler

from registration import *
from subscription import *
from take_book import *
from db_func import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN: str = '5224259246:AAFNi4jQBZ19CSuiqkB9kYNw6mz6h-lqI7E'


def start_messaging(update: Update, context: Any) -> int:
    """Function greets the user"""
    update.message.reply_text('Вас приветствует телеграм-бот \n'
                              'электронной библиотеки LibLab👋\n'
                              'В нашей библиотеке представлена внушительная коллекция книг на любой вкус 👍\n'
                              'Желаю вам приятного чтения 🤓')
    methods_func(update, context)
    us_id = update.message.from_user.id
    add_item(us_id)


def help_func(update: Update, context: Any) -> None:
    """Function gives some important information"""
    update.message.reply_text('Вам нужна помомщь❓ \nДавайте я вам расскажу о том, что я умею: \n'
                              '📖take_book - этот метод позволяет пользователю получить книгу\n'
                              '📅subscription - этот метод помогает пользователю оформить подписку\n'
                              '💻registration - этот метод помогает пользователю зарегестрироваться в нашей библиотеке\n'
                              'Куда отправимся❓')
    time.sleep(2)
    methods_func(update, context)


def methods_func(update: Update, context: Any) -> None:
    """Function gets methods"""
    methods_reply_keyboard = [['📖take_book', '📅subscription'], ['❓help', '💻registration']]
    methods_markup = ReplyKeyboardMarkup(methods_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text('Вот действующие методы:', reply_markup=methods_markup)


class User:
    def __init__(self, id, name_surname, registration, subscription):
        self.id = id
        self.name_surname = name_surname
        self.registration = registration
        self.subscription = subscription

    def begin_registration_user_func(self: Update, context: Any):
        flag: bool = begin_registration_user(self, context)
        if flag:
            return 1
        methods_func(self, context)
        return ConversationHandler.END

    def registration_handle_user_data_func(self: Update, context: Any):
        flag: bool = registration_handle_user_data(self, context)
        if flag:
            time.sleep(2)
            methods_func(self, context)
            return ConversationHandler.END
        return 1

    def begin_subscription_user_func(self: Update, context: Any):
        flag: bool = subscription_user(self, context)
        if not flag:
            time.sleep(2)
            methods_func(self, context)
            return ConversationHandler.END
        else:
            active = subscription_activated_check(self, context)
            if active:
                return 1
            else:
                subscription_need_active(self, context)
                return 2

    def subscription_need_ans_func(self: Update, context: Any):
        if subscription_need_ans(self, context):
            pass
        else:
            time.sleep(2)
            methods_func(self, context)
        return ConversationHandler.END

    def subscription_not_need_active_func(self: Update, context: Any):
        ...
        # Дописать Алмазу функцию обновления подписки - сначала выводим даты,
        # а потом спрашиваем о продлении, если да - то двигаем дату окончания на месяц вперед,
        # функция на сдвиг месяца написана, а для обновления даты там тоже
        # выделена функция, в остальном юзай дальше этот ConversationHandler и пиши функции,

    def take_book_func(self: Update, context: Any):
        take_book_user(self, context)
        return 1

    def take_book_1_func(self: Update, context: Any):
        take_book_1_user(self, context)
        return ConversationHandler.END


class Subscription:
    def __init__(self, id, exists_since, valid_until, activity):
        self.id = id
        self.exists_since = exists_since
        self.valid_until = valid_until
        self.activity = activity

    def renew_dates_func(self: Update, context: CallbackContext):
        renew_dates_user(self, context)

    # checking correction pay
    def precheckout_callback(self: Update, context: Any) -> None:
        query = self.pre_checkout_query
        if query.invoice_payload != 'Custom-Payload':
            # answer False pre_checkout_query
            query.answer(ok=False, error_message="Упс...Какая-то ошибка.")
        else:
            query.answer(ok=True)

    # message after pay
    def successful_payment_callback(self: Update, context: Any) -> None:
        """Confirms the successful payment."""
        # do something after successfully receiving payment?
        self.message.reply_text("Теперь у вас есть подписка!")
        time.sleep(2)
        new_dates_user(self, context, self.message.from_user.id)
        methods_func(self, context)


class Book:
    def __init__(self, id, author, genre, availability):
        self.id = id
        self.author = author
        self.genre = genre
        self.availability = availability


def command(update: Update, context: Any):
    command = update.message.text
    update.message.reply_text('Увы☹, но я тебя не понимаю.\nПопробуй воспользоваться этими командами👇')
    time.sleep(1)
    help_func(update, context)


def stop(update: Update, context: Any):
    update.message.reply_text(
        "Пока-пока")


def main() -> None:
    """main function organizes work of our bot"""
    updater: Updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_messaging))

    dispatcher.add_handler(PrefixHandler('📃', 'methods', methods_func))
    dispatcher.add_handler(PrefixHandler('❓', 'help', help_func))
    conv_handler = ConversationHandler(
        entry_points=[PrefixHandler('📖', 'take_book', User.take_book_func)],
        states={
            1: [MessageHandler(Filters.text, User.take_book_1_func, pass_user_data=True)]
        }, fallbacks=[CommandHandler('stop', stop)]
    )
    dispatcher.add_handler(conv_handler)

    conv_handler_registration = ConversationHandler(
        entry_points=[PrefixHandler('💻', 'registration', User.begin_registration_user_func)],
        states={
            1: [MessageHandler(Filters.text, User.registration_handle_user_data_func, pass_user_data=True)]
        }, fallbacks=[CommandHandler('stop', stop)])
    dispatcher.add_handler(conv_handler_registration)

    conv_handler_subscription = ConversationHandler(
        entry_points=[PrefixHandler('📅', 'subscription', User.begin_subscription_user_func)],
        states={
            1: [MessageHandler(Filters.text, User.subscription_not_need_active_func, pass_user_data=True)],
            2: [MessageHandler(Filters.text, User.subscription_need_ans_func, pass_user_data=True)]
        }, fallbacks=[CommandHandler('stop', stop)])
    dispatcher.add_handler(conv_handler_subscription)

    # don't touch!
    dispatcher.add_handler(PreCheckoutQueryHandler(Subscription.precheckout_callback))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, Subscription.successful_payment_callback))
    dispatcher.add_handler(MessageHandler(Filters.text, command, pass_user_data=True))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
