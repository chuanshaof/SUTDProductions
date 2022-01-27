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

add_details = ["Name: ",
               "Description: ",
               "POC: ",
               "Venue: ",
               "Project Purpose: ",
               "Inspiration: ",
               "Roles needed: ",
               "Production Deadline: ",
               "Project Requirement: ",
               "Team: "]


# Adding Projects
# ---------------------------------------------------------------------------------------------#
def add(update: Update, context: CallbackContext) -> int:
    text = "Please enter the new project details in the format of:\n" \
           "(For empty entries, put NIL)\n\n"
    for every in range(len(add_details)):
        text = text + add_details[every] + "\n"
    update.message.reply_text(text,
                              parse_mode=ParseMode.HTML)

    return globals.ADD


def confirm(update: Update, context: CallbackContext) -> int:
    context.user_data["temp_project"] = list()

    for every in range(len(add_details)):
        if add_details[every] not in update.message.text:
            update.message.reply_text("Project details are incomplete, please use /add to retry accordingly "
                                      "to the example below:\n\n"
                                      f"Name: SUTD Productions\n"
                                      f"Details: Club\n"
                                      f"POC: NIL\n"
                                      f"Venue: SUTD\n"
                                      f"Project Purpose: NIL\n"
                                      f"Inspiration: NIL\n"
                                      f"Roles needed: Excos\n"
                                      f"Production Deadline: 2021\n"
                                      f"Project Requirement: NIL\n"
                                      f"Team: Jean, Noah",
                                      parse_mode=ParseMode.HTML)
            return ConversationHandler.END

        if every == 9:
            found = update.message.text.find(add_details[every]) + len(add_details[every])
            context.user_data["temp_project"].append(update.message.text[found:])
        else:
            found = update.message.text.find(add_details[every]) + len(add_details[every])
            next_find = update.message.text.find(add_details[every + 1])
            entry = update.message.text[found:next_find-1]
            if not entry:
                update.message.reply_text("Project details are incomplete, please use /add to retry accordingly "
                                          "to the example below:\n\n"
                                          f"Name: SUTD Productions\n"
                                          f"Details: Club\n"
                                          f"POC: NIL\n"
                                          f"Venue: SUTD\n"
                                          f"Project Purpose: NIL\n"
                                          f"Inspiration: NIL\n"
                                          f"Roles needed: Excos\n"
                                          f"Production Deadline: 2021\n"
                                          f"Project Requirement: NIL\n"
                                          f"Team: Jean, Noah",
                                          parse_mode=ParseMode.HTML)
                return ConversationHandler.END

            if every == 0:
                if len(entry) > 50 or "\n" in entry:
                    update.message.reply_text("Please enter a valid project name that is less than 50 characters long "
                                              "and does not contain a new line")
                    return ConversationHandler.END

                projects = firebase.db.child("project").get().val()

                if projects is not None:
                    for each in projects:
                        if each == update.message.text:
                            update.message.reply_text(
                                "Project name has been taken, please retry with a new project name.")
                            return ConversationHandler.END

            context.user_data["temp_project"].append(entry)

    keyboard = [[InlineKeyboardButton("Yes", callback_data="Yes")],
                [InlineKeyboardButton("No", callback_data="No")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Please confirm project details.\n\n"
                         + view_projects(context.user_data["temp_project"]),
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML)

    # Uses /add functions
    return globals.PROJECT_CONFIRM

# Adding Projects (CONFIRM)
def project_confirm(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == "Yes":
        query.edit_message_text(f"Successfully added {context.user_data['temp_project'][0]}.")
        firebase.db.child("project").child(context.user_data["temp_project"][0].replace("?", "%3F"))\
            .set(context.user_data["temp_project"])
        return ConversationHandler.END
    else:
        query.edit_message_text("Cancelled.")
        return ConversationHandler.END
