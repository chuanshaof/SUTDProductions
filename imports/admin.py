from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

from imports import globals
import firebase


# Admin Verification
# ---------------------------------------------------------------------------------------------#
def admin(update: Update, context: CallbackContext) -> int:
    admins = firebase.db.child("admin").get().val()

    if admins is not None and update.message.from_user.id in admins:
        update.message.reply_text("Already verified.\n\n"
                                  "You can now utilize the following commands:\n\n"
                                  "/add - Add projects to the list\n"
                                  "/remove - Remove projects from the list\n"
                                  "/edit - Edit project details\n"
                                  "/announce - Send a message to all subscribers\n"
                                  "/check_subs - Check who is subscribed to the bot")
        return ConversationHandler.END
    else:
        update.message.reply_text("Enter the admin code")
        return globals.WAIT_CODE


# Admin Verification, step 2
def verify(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    code = ***REMOVED***

    if user_input == code:
        update.message.reply_text("Verified, you can now utilize the following commands:\n\n"
                                  "/add - Add projects to the list\n"
                                  "/remove - Remove projects from the list\n"
                                  "/edit - Edit project details\n"
                                  "/announce - Send a message to all subscribers\n"
                                  "/check_subs - Check who is subscribed to the bot")
        admins = firebase.db.child("admin").get().val()

        if admins == None:
            admins = [update.message.from_user.id]
        else:
            admins.append(update.message.from_user.id)
        firebase.db.child("admin").set(admins,  firebase.user['idToken'])
    else:
        update.message.reply_text("Invalid")

    return ConversationHandler.END