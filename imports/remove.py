from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

from imports.bits import view_projects
from imports import globals
import firebase


# Removing projects
# ---------------------------------------------------------------------------------------------#
def remove(update: Update, context: CallbackContext) -> None:
    admins = firebase.db.child("admin").get().val()
    projects = firebase.db.child("project").get().val()

    if admins is not None and update.message.from_user.id in admins:
        if projects == None:
            update.message.reply_text("Sorry, there are no projects at the moment!")
            return ConversationHandler.END
        else:
            keyboard = list()
            for each in projects:
                project = InlineKeyboardButton(each, callback_data=each)
                keyboard.append([project])

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Please select the project name you want to remove.", reply_markup=reply_markup)
            return globals.REMOVE
    else:
        return


# Remove project (CONFIRM)
def remove_confirm(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    projects = firebase.db.child("project").get().val()

    for each in projects:
        # Each[0] represents the name
        if query.data == each:
            keyboard = [[InlineKeyboardButton("Yes", callback_data="Y" + each)],
                        [InlineKeyboardButton("No", callback_data="N" + each)]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            query.edit_message_text(f"{view_projects(projects[each])}\n"
                                    f"Please confirm project removal.",
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML)
        if query.data == "Y" + each:
            query.edit_message_text(f"{each} has been successfully removed.")
            firebase.db.child("project").child(each.replace("?", "%3F")).remove(firebase.user['idToken'])
            return ConversationHandler.END
        elif query.data == "N" + each:
            query.edit_message_text("Cancelled.")
            return ConversationHandler.END
