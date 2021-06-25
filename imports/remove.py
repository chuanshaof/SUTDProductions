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
            projects = format_project_list(update, context)
            keyboard = list()

            for each in projects:
                project = InlineKeyboardButton(each, callback_data=each)
                keyboard.append([project])

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Please select the project name you want to remove.", reply_markup=reply_markup)
            return globals.REMOVE


# Remove project (CONFIRM)
def remove_confirm(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    keyboard = [[InlineKeyboardButton("Yes", callback_data="Y")],
                [InlineKeyboardButton("No", callback_data="N")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    for each in context.bot_data["projects"]:
        # Each[0] represents the name
        if query.data == each[0]:
            query.edit_message_text(f"{view_projects(each)}\n"
                                    f"Please confirm project removal.",
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML)
        if query.data == "Y":
            query.edit_message_text(f"{each[0]} has been successfully removed.")
            context.bot_data["projects"].remove(each)
            return ConversationHandler.END
        elif query.data == "N":
            query.edit_message_text("Cancelled.")
            return ConversationHandler.END


# Random stuff
# ---------------------------------------------------------------------------------------------#
# Returns a list, used in multiple places
def format_project_list(update: Update, context: CallbackContext) -> list:
    if "projects" not in context.bot_data:
        context.bot_data["projects"] = list()
        return list()
    list_of_names = list()
    for each in context.bot_data["projects"]:
        list_of_names.append(each[0])
    return list_of_names