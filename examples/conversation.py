from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, PicklePersistence, \
    ConversationHandler

WAIT_HEIGHT, WAIT_WEIGHT = range(2)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("What is your height?")
    return WAIT_HEIGHT


def ask_weight(update: Update, context: CallbackContext):
    # not shown: persist height
    update.message.reply_text("What is your weight?")
    return WAIT_WEIGHT


def calculate_bmi(update: Update, context: CallbackContext):
    # not shown: retrieve height in persistence and weight from the message
    update.message.reply_text("Your BMI is X")
    return ConversationHandler.END


updater = Updater('YOUR_BOT_TOKEN_HERE')

updater.dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler("start", start)
    ],
    states={
        WAIT_HEIGHT: [MessageHandler(Filters.text, ask_weight)],
        WAIT_WEIGHT: [MessageHandler(Filters.text, calculate_bmi)]
    },
    fallbacks=[]
))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    updater.start_polling()
    updater.idle()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
