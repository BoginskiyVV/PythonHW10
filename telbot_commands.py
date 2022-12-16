from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from logger import log
from calc import calc_data, check_data


FIRST, SECOND, CALC = range(3)
ONE, TWO = range(2)

def start(update, _):
    user = update.message.from_user
    log(update, f'Пользователь начал разговор {update.message.text}')
    keyboard = [
        [
            InlineKeyboardButton("Рассчитать выражение",
                                 callback_data=str(ONE)),
            InlineKeyboardButton("Посмотреть лог файл",
                                 callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text=f'''Приветствую, {user.first_name}! Я калькулятор-бот,
        \nпосчитаю выражение с целыми, рациональными и комплексными числами.
        Команда /cancel, чтобы прекратить.
        \nВыберите из предложенных пунктов меню:''', reply_markup=reply_markup
    )
    return FIRST


def start_over(update, _):
    query = update.callback_query
    log(update, 'Пользователь вернулся в меню')
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Рассчитать выражение",
                                 callback_data=str(ONE)),
            InlineKeyboardButton("Посмотреть лог файл",
                                 callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Выберите из предложенных пунктов меню:", reply_markup=reply_markup)
    return FIRST


def input_data(update, _):
    log(update,  'Выбран пункт меню: "Рассчитать выражение"')
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='''Пример: 2.54-1.05*6.45 и т.п.\n Введите выражение в поле для сообщений: ''')
    return CALC


def view_result(update, _):
    log(update, f'Пользователь ввел выражение {update.message.text}')
    user_input = update.message.text
    if isinstance(check_data(user_input), tuple):
        try:
            t, value = check_data(user_input)
            result = calc_data(t, value)
        except:
            result = 'Некорректное выражение'
    else:
        result = check_data(user_input)

    log(update, f'Выдаем результат: {result}')

    keyboard = [
        [
            InlineKeyboardButton("Вернуться в Меню", callback_data=str(ONE)),
            InlineKeyboardButton("Нет, с меня хватит ...",
                                 callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text=f"{result}")
    update.message.reply_text(
        text="Начать сначала?", reply_markup=reply_markup
    )

    return SECOND


def view_log(update, context):
    log(update, 'Выдаем лог-файл')

    """Показ выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Вернуться в Меню", callback_data=str(ONE)),
            InlineKeyboardButton("Выход ...", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.bot.send_document(chat_id=update.effective_chat.id, document=open('calc_bot.txt', 'rb'), caption='Файл лога',
                            )
    context.bot.send_message(chat_id=update.effective_chat.id,
                        text="Начать сначала?", reply_markup=reply_markup)
    return SECOND


def end(update, _):
    log(update, 'Пользователь завершил разговор')
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Увидимся в другой раз!")
    return ConversationHandler.END


def cancel(update, _):
    user = update.message.from_user
    log(update, 'Пользователь отменил разговор')
    update.message.reply_text(f'{user.first_name}, пока!')
    return ConversationHandler.END
