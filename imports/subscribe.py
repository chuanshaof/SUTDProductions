from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence


def subscribe(update: Update, context: CallbackContext) -> None:
    if "subscribe" not in context.bot_data:
        context.bot_data["subscribe"] = list()

    if any(update.message.from_user.id in sl for sl in context.bot_data["subscribe"]):
        for each in context.bot_data["subscribe"]:
            if each[0] == update.message.from_user.id:
                context.bot_data["subscribe"].remove(each)
                update.message.reply_text("Unsubscribed from SUTDProductions, we hope to see you again!")
                return
    else:
        context.bot_data["subscribe"].append([update.message.from_user.id, update.message.from_user.username])
        update.message.reply_text("Subscribed to SUTDProductions.")
        return