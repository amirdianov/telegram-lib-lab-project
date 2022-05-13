"""
Telegram bot LibLab
"""
import time

from telegram import ShippingOption, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import PreCheckoutQueryHandler, CallbackQueryHandler

from registration import *
from subscription import *
from take_book import *
from db_func import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN: str = '5153990837:AAHVrwUUYPFwfQlGv37TeZ2A3dsW1MYWRis'


def start_messaging(update: Update, context: Any) -> int:
    """Function greets the user"""
    update.message.reply_text('Вас приветствует телеграм-бот \n'
                              'электронной библиотеки LibLab👋\n'
                              'В нашей библиотеке представлена внушительная коллекция книг на любой вкус 👍\n'
                              'Желаю вам приятного чтения 🤓')
    methods_func(update, context)
    us_id = update.message.from_user.id
    User.User_id = us_id
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
    CRITERION: dict = {
        'title': 'название',
        'genre': 'жанр',
        'author': 'автора',
    }
    User_id = None

    def __init__(self, id, name_surname, registration, subscription):
        self.id = id
        self.name_surname = name_surname
        self.registration = registration
        self.subscription = subscription

    def begin_registration_user_func(self: Update, context: Any):
        # us_id = self.message.from_user.id
        # User.User_id = us_id
        flag: bool = begin_registration_user(self, context)
        if flag:
            return 1
        time.sleep(2)
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
        # us_id = self.message.from_user.id
        # User.User_id = us_id
        flag: bool = subscription_user(self, context)
        if not flag:
            time.sleep(2)
            methods_func(self, context)
            return ConversationHandler.END
        else:
            active = subscription_activated_check(self, context)
            if active:
                subscription_not_need_active(self, context)
                return 1
            else:
                subscription_need_active(self, context)
                return 2

    def subscription_need_ans_func(self: Update, context: Any):
        if subscription_need_ans(self, context):
            return ConversationHandler.END
        else:
            time.sleep(2)
            methods_func(self, context)
        return ConversationHandler.END

    def subscription_not_need_active_func(self: Update, context: Any):
        if subscription_not_need_active_ans(self, context):
            return ConversationHandler.END
        else:
            time.sleep(2)
            methods_func(self, context)
        return ConversationHandler.END

    def begin_take_book_user_func(self: Update, context: Any):
        # us_id = self.message.from_user.id
        # User.User_id = us_id
        if take_book_user(self, context):
            take_book_type(self, context)
            return 1
        else:
            time.sleep(2)
            methods_func(self, context)

    def take_book_1_func(self: Update, context: Any):
        print('Стадия take_book_1_func')
        ans = self.message.text
        # здесь надо не завершать ConversationHandler, а продолжить
        # чтобы дальше писать свой блок взятия книги по типу
        if ans == 'title' or ans == 'genre':
            flag = User.find_book_function(self, context)
            return flag
        else:
            # Можно как то так продолжить
            self.message.reply_text('Что - то пошло не так и бот сломался...')

    def find_book_function(self: Update, context: Any):
        inner_find_book_function(self, context, User.CRITERION[self.message.text])
        return User.CRITERION[self.message.text]

    def take_book_title(self: Update, context: Any):
        print('Стадия take_book_title')
        print('Message text:', self.message.text)
        inner_take_book(self, context, self.message.text.capitalize(), 'title')
        delete_second_telegram_message(context.user_data['message'])
        return 'checking_stage'

    def take_book_genre(self: Update, context: Any):
        print('Стадия take_genre')

    def take_book_genre_1(self: Update, context: Any, name_genre: Any):
        create_buttons_book(self, context, name_genre, User.User_id)
        delete_second_telegram_message(context.user_data['message'])
        return 'checking_stage'

    def take_book_author(self: Update, context: Any):
        ...
        return ConversationHandler.END

    def take_book_rating(self: Update, context: Any):
        ...
        return ConversationHandler.END

    def find_book_function_for_inline(self, context: Any):
        print('Стадия find_book_function_for_inline')
        print('context.user_data', context.user_data['criterion'])
        response = self.callback_query
        inner_find_book_function_for_inline(response, context)
        response.answer()
        delete_telegram_message(response)
        return context.user_data['criterion']

    def check_book(self: Update, context: Any):
        print('Стадия check_book')
        return User.inner_check_book(self, context)

    def handle_subscription_case(self: Update, context: Any):
        print('Стадия handle_subscription_case')
        ReplyKeyboardRemove()
        inner_handle_subscription_case(self, context)
        return ConversationHandler.END

    def inner_check_book(self, context: Any):
        print("callback_query:", self.callback_query.data)
        response = self.callback_query
        response.answer()
        if response.data == 'need_to_get_subscription':
            reply_buttons = [['😍Да', 'Нет...']]
            reply_button_markup = ReplyKeyboardMarkup(reply_buttons, one_time_keyboard=True, resize_keyboard=True)
            response.message.reply_text('К сожалению, эта книга доступна только по подписке😔\n'
                                        'Желаете ли вы её оформить?', reply_markup=reply_button_markup)
            return 'subscribe_stage'
        elif response.data == 'back_to_prev_state':
            delete_telegram_message(response)
            return User.find_book_function_for_inline(self, context)
        elif response.data == 'back_to_prev_state_1':
            delete_telegram_message(response)
            return User.find_book_function_for_inline(self, context)
        elif response.data == 'back_to_main_menu':
            delete_telegram_message(response)
            delete_second_telegram_message(context.user_data['message'])
            methods_func(response, context)
            return ConversationHandler.END

    def handle_coming_back(self, context):
        print('Стадия handle_coming_back_new')
        print(self.callback_query.data)
        response = self.callback_query
        print('id:', self.callback_query.message.chat.id)
        if response.data == 'back_to_main_menu':
            response.answer()
            delete_second_telegram_message(context.user_data['message'])
            delete_telegram_message(response)
            methods_func(response, context)
            return ConversationHandler.END
        elif response.data == 'back_to_prev_state':
            response.answer()
            delete_telegram_message(response)
            return User.begin_take_book_user_func(response, context)
        elif response.data == 'back_to_prev_state_1':
            response.answer()
            delete_telegram_message(response)
            return User.take_book_genre(response, context)
        else:
            return User.take_book_genre_1(response, context, response.data)


class Subscription:
    def __init__(self, id, exists_since, valid_until, activity):
        self.id = id
        self.exists_since = exists_since
        self.valid_until = valid_until
        self.activity = activity

    def renew_dates_func(self: Update, context: CallbackContext):
        pass

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
        self.message.reply_text("Читайте с удовольствием!📚")
        time.sleep(2)
        user_id = self.message.from_user.id
        if get_items('exists_since', 'Subscription', 'telegram_id',
                     user_id)[0] is not None:
            renew_dates_user(self, context, user_id)
        else:
            new_dates_user(self, context, user_id)
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
    dispatcher.add_handler(CommandHandler('methods', start_messaging))

    # dispatcher.add_handler(PrefixHandler('📃', 'methods', methods_func))
    dispatcher.add_handler(PrefixHandler('❓', 'help', help_func))
    conv_handler = ConversationHandler(
        entry_points=[PrefixHandler('📖', 'take_book', User.begin_take_book_user_func),
                      CallbackQueryHandler(User.find_book_function_for_inline, pass_user_data=True)],
        states={
            1: [MessageHandler(Filters.text, User.take_book_1_func, pass_user_data=True)],
            'название': [MessageHandler(Filters.text, User.take_book_title, pass_user_data=True),
                         CallbackQueryHandler(User.handle_coming_back, pass_user_data=True)],
            'жанр': [MessageHandler(Filters.text, User.take_book_genre, pass_user_data=True),
                     CallbackQueryHandler(User.handle_coming_back, pass_user_data=True)],
            'автора': [MessageHandler(Filters.text, User.take_book_author, pass_user_data=True)],
            'rating': [MessageHandler(Filters.text, User.take_book_rating, pass_user_data=True)],
            'checking_stage': [CallbackQueryHandler(User.check_book, pass_user_data=True)],
            'subscribe_stage': [MessageHandler(Filters.text, User.handle_subscription_case, pass_user_data=True)]
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
