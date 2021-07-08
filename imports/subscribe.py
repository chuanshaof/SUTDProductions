from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

import firebase


def subscribe(update: Update, context: CallbackContext) -> None:
    subscribers = firebase.db.child("subscriber").get().val()

    if subscribers != None:
        for each in subscribers:
            if each == str(update.message.from_user.id):
                firebase.db.child("subscriber").child(str(update.message.from_user.id)).remove()
                update.message.reply_text("Unsubscribed from SUTDProductions, we hope to see you again!")
                return

    new_sub = {update.message.from_user.id: update.message.from_user.username}
    firebase.db.child("subscriber").update(new_sub)
    update.message.reply_text("Subscribed to SUTDProductions bot.")
    return
