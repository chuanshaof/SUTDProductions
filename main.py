from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters


def hello(update: Update, context: CallbackContext) -> None:
    print(update)
    update.message.reply_text(f'Hello!')


updater = Updater('BOT_TOKEN_HERE')

updater.dispatcher.add_handler(MessageHandler(Filters.update, callback=hello))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    updater.start_polling()
    updater.idle()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
