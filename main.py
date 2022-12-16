from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                          ConversationHandler, MessageHandler, Filters)
from telbot_commands import *
import config


FIRST, SECOND, CALC = range(3)
ONE, TWO = range(2)

updater = Updater(config.Token)
dispatcher = updater.dispatcher


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FIRST: [
              CallbackQueryHandler(input_data, pattern='^' + str(ONE) + '$'),
              CallbackQueryHandler(view_log, pattern='^' + str(TWO) + '$'),
        ],
        CALC: [MessageHandler(Filters.text & ~Filters.command, view_result)],
        SECOND: [
            CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
            CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()

print('Server start')
