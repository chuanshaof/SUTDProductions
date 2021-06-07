from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, PicklePersistence, \
    ConversationHandler

WAIT_HEIGHT, WAIT_WEIGHT = range(2)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("What is your height?")
    return WAIT_HEIGHT


def ask_weight(update: Update, context: CallbackContext):
    # not shown: persist height
    user_input = update.message.text
    if not user_input.isnumeric():
        update.message.reply_text("Please give me a number.")
        return None

    context.user_data["height"] = int(user_input)
    update.message.reply_text("What is your weight?")
    return WAIT_WEIGHT


def calculate_bmi(update: Update, context: CallbackContext):
    # not shown: retrieve height in persistence and weight from the message
    user_input = update.message.text
    if not user_input.isnumeric():
        update.message.reply_text("Please give me a number.")
        return None

    height = context.user_data["height"]
    weight = int(user_input)
    bmi = weight/ ((height / 100) ** 2)

    update.message.reply_text(f"Your BMI is {round(bmi,2)}")
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
