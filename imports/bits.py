from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

import firebase


# Check subscribed members
def check_subs(update: Update, context: CallbackContext) -> None:
    admins = firebase.db.child("admin").get().val()
    if admins is not None and update.message.from_user.id in admins:
        subs = ""
        subscribers = firebase.db.child("subscriber").get().val()
        print(subscribers)
        for each in subscribers:
            subs = subs + "@" + subscribers[each] + "\n"
        update.message.reply_text(subs)
    return


# Clearing of admins
def clear_admins(update: Update, context: CallbackContext) -> None:
    admins = firebase.db.child("admin").get().val()
    if admins is not None and update.message.from_user.id in admins:
        firebase.db.child("admin").remove()
        update.message.reply_text("Admin list cleared.")


# Returns a formatted string, used in multiple places
def view_projects(project: list) -> str:
    view_proj = f"<b>{project[0]}</b>\n" \
                f"<i>{project[1]}</i>\n" \
                f"POC: {project[2]}\n" \
                f"Venue: {project[3]}\n" \
                f"Project Purpose: {project[4]}\n" \
                f"Inspiration: {project[5]}\n" \
                f"Roles needed: {project[6]}\n" \
                f"Production Deadline: {project[7]}\n" \
                f"Project Requirement: {project[8]}\n" \
                f"Team: {project[9]}\n"
    return view_proj
