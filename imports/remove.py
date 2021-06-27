from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

from imports.bits import view_projects
from imports import globals


# Removing projects
# ---------------------------------------------------------------------------------------------#
def remove(update: Update, context: CallbackContext) -> None:
    if "admin" not in context.bot_data:
        context.bot_data["admin"] = list()

    if update.message.from_user.id not in context.bot_data["admin"]:
        return
    else:
        if "projects" not in context.bot_data or len(context.bot_data["projects"]) == 0:
            context.bot_data["projects"] = list()
            update.message.reply_text("Sorry, there are no projects at the moment!")
            return
        else:
            keyboard = list()

            for each in context.bot_data["projects"]:
                project = InlineKeyboardButton(each[0], callback_data=each[0])
                keyboard.append([project])

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Please select the project name you want to remove.", reply_markup=reply_markup)
            return globals.REMOVE


# Remove project (CONFIRM)
def remove_confirm(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    for each in context.bot_data["projects"]:
        # Each[0] represents the name
        if query.data == each[0]:
            keyboard = [[InlineKeyboardButton("Yes", callback_data="Y" + each[0])],
                        [InlineKeyboardButton("No", callback_data="N" + each[0])]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            query.edit_message_text(f"{view_projects(each)}\n"
                                    f"Please confirm project removal.",
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML)
        if query.data == "Y" + each[0]:
            query.edit_message_text(f"{each[0]} has been successfully removed.")
            context.bot_data["projects"].remove(each)
            return ConversationHandler.END
        elif query.data == "N" + each[0]:
            query.edit_message_text("Cancelled.")
            return ConversationHandler.END
