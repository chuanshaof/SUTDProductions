from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

import os

from imports import globals
import firebase

TOKEN = os.environ["API_KEY"]
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)


def announce(update: Update, context: CallbackContext) -> None:
    admins = firebase.db.child("admin").get().val()
    subscribers = firebase.db.child("subscriber").get().val()
    if admins is not None and update.message.from_user.id in admins:
        if subscribers is not None:
            for each in subscribers:
                update.message.reply_text("Enter the message to announce.")
                return globals.ANNOUNCE_QUERY
        update.message.reply_text("No one is subscribed to the bot.")
        return
    return


def announcement_confirm(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Confirm", callback_data="Y")],
                [InlineKeyboardButton("Cancel", callback_data="N")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    global announce_message
    announce_message = update.message.text

    bot.sendMessage(chat_id=update.message.chat_id,
                    text=f"Confirm announcement message:\n\n"
                         f"{update.message.text}",
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup)
    return globals.ANNOUNCE


def announcement(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    subscribers = firebase.db.child("subscriber").get().val()

    if query.data == "Y":
        for each in subscribers:
            forward_to = str(each)
            try:
                bot.sendMessage(chat_id=forward_to,
                                text=announce_message,
                                parse_mode=ParseMode.HTML)
            except:
                print(each + " has blocked the bot.")
                firebase.db.child("subscriber").child(str(update.message.from_user.id)).remove()

        query.edit_message_text("Successfully announced to subscribers.")
        return ConversationHandler.END
    elif query.data == "N":
        query.edit_message_text("Cancelled.")
        return ConversationHandler.END
