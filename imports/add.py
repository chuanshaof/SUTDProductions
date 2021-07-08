from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

import os

from imports.bits import view_projects
from imports import globals
import firebase

TOKEN = os.environ["API_KEY"]
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)


# Adding Projects
# ---------------------------------------------------------------------------------------------#
def add(update: Update, context: CallbackContext) -> int:
    admins = firebase.db.child("admin").get().val()

    if admins is not None and update.message.from_user.id in admins:
        firebase.db.child(update.message.from_user.id).set(list())
        update.message.reply_text("Please enter project name, maximum of 50 characters all in one line.")
        return globals.PROJECT_NAME
    else:
        return ConversationHandler.END


# Adding Projects (TITLE)
def project_name(update: Update, context: CallbackContext) -> int:
    if not update.message.text or len(update.message.text) > 50 or "\n" in update.message.text:
        update.message.reply_text("Please enter a valid project name.")
        return globals.PROJECT_NAME

    projects = firebase.db.child("project").get().val()

    if projects is not None:
        for each in projects:
            if each == update.message.text:
                update.message.reply_text("Project name has been taken, please key in a new project name.")
                return globals.PROJECT_NAME

    context.user_data["temp_project"] = list()
    context.user_data["temp_project"].append(update.message.text)
    update.message.reply_text("Please enter project description.")
    return globals.PROJECT_DESCRIPTION


# Adding Projects (DETAILS)
def project_description(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project description.")
        return globals.PROJECT_DESCRIPTION
    else:
        context.user_data["temp_project"].append(update.message.text)
        update.message.reply_text("Please enter project POC.")
        return globals.PROJECT_POC


# Adding Projects (DETAILS)
def project_poc(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project POC.")
        return globals.PROJECT_POC
    else:
        context.user_data["temp_project"].append(update.message.text)
        update.message.reply_text("Please enter project venue.")
        return globals.PROJECT_VENUE


# Adding Projects (DETAILS)
def project_venue(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project venue.")
        return globals.PROJECT_VENUE
    else:
        context.user_data["temp_project"].append(update.message.text)
        update.message.reply_text("Please enter project purpose.")
        return globals.PROJECT_PURPOSE


# Adding Projects (DETAILS)
def project_purpose(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project purpose.")
        return globals.PROJECT_PURPOSE
    else:
        context.user_data["temp_project"].append(update.message.text)
        update.message.reply_text("Please enter project inspiration.")
        return globals.PROJECT_INSPIRATION


# Adding Projects (INSPIRATION)
def project_inspiration(update: Update, context: CallbackContext) -> int:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project inspiration.")
        return globals.PROJECT_DESCRIPTION
    else:
        context.user_data["temp_project"].append(update.message.text)
        update.message.reply_text("Please enter project roles.")
        return globals.PROJECT_ROLES


# Adding Projects (ROLES)
def project_roles(update: Update, context: CallbackContext) -> int:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project roles.")
        return globals.PROJECT_ROLES
    else:
        context.user_data["temp_project"].append(update.message.text)
        update.message.reply_text("Please enter project deadline.")
        return globals.PROJECT_DEADLINE


# Adding Projects (DEADLINE)
def project_deadline(update: Update, context: CallbackContext) -> int:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project deadline.")
        return globals.PROJECT_DEADLINE
    else:
        context.user_data["temp_project"].append(update.message.text)
        update.message.reply_text("Please enter project requirement.")
        return globals.PROJECT_REQUIREMENTS


# Adding Projects (DEADLINE)
def project_requirement(update: Update, context: CallbackContext) -> int:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project requirement.")
        return globals.PROJECT_REQUIREMENTS
    else:
        context.user_data["temp_project"].append(update.message.text)
        update.message.reply_text("Please enter project team.")
        return globals.PROJECT_TEAM


# Adding Projects (TEAM)
def project_team(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project team.")
        return globals.PROJECT_TEAM
    else:
        context.user_data["temp_project"].append(update.message.text)

    keyboard = [[InlineKeyboardButton("Yes", callback_data="Yes")],
                [InlineKeyboardButton("No", callback_data="No")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Please confirm project details.\n\n"
                         + view_projects(context.user_data["temp_project"]),
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML)

    return globals.PROJECT_CONFIRM


# Adding Projects (CONFIRM
def project_confirm(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == "Yes":
        query.edit_message_text(f"Successfully added {context.user_data['temp_project'][0]}.")
        firebase.db.child("project").child(context.user_data["temp_project"][0]).set(context.user_data["temp_project"])
        return ConversationHandler.END
    else:
        query.edit_message_text("Cancelled.")
        return ConversationHandler.END
