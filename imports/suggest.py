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


# Suggesting Projects
# ---------------------------------------------------------------------------------------------#
def suggest(update: Update, context: CallbackContext) -> int:
    text = "Suggest a project in the format of:\n" \
           "(For empty entries, put NIL)\n\n"
    for every in range(len(globals.project_details)):
        text = text + globals.project_details[every] + "\n"
    update.message.reply_text(text,
                              parse_mode=ParseMode.HTML)

    return globals.SUGGEST


def confirm(update: Update, context: CallbackContext) -> int:
    context.user_data["temp_project"] = list()

    for every in range(len(globals.project_details)):
        if globals.project_details[every] not in update.message.text:
            update.message.reply_text("Project details are incomplete, please use /block_project to retry accordingly "
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
            found = update.message.text.find(globals.project_details[every]) + len(globals.project_details[every])
            context.user_data["temp_project"].append(update.message.text[found:])
        else:
            found = update.message.text.find(globals.project_details[every]) + len(globals.project_details[every])
            next_find = update.message.text.find(globals.project_details[every + 1])
            entry = update.message.text[found:next_find-1]
            if not entry:
                update.message.reply_text("Project details are incomplete, please use /block_project to retry accordingly "
                                          "to the example below:\n\n"
                                          f"Name: SUTD Productions\n"
                                          f"Description: Club\n"
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

            context.user_data["temp_project"].append(entry)

    keyboard = [[InlineKeyboardButton("Yes", callback_data="Yes")],
                [InlineKeyboardButton("No", callback_data="No")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Please confirm project details.\n\n"
                         + view_projects(context.user_data["temp_project"]),
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML)

    return globals.SUGGEST_CONFIRM


# Suggesting Projects (CONFIRM)
def project_confirm(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == "Yes":
        NOAH = 262240949
        bot.sendMessage(chat_id=NOAH,
                        text=f"Hi, @{query.from_user.username} has suggested the following project.\n\n"
                             + view_projects(context.user_data["temp_project"]),
                        parse_mode=ParseMode.HTML)

        query.edit_message_text("Thank you for your suggestion!\n"
                                "Your interest has been noted and we will be getting back to you shortly.")
        return ConversationHandler.END
    else:
        query.edit_message_text("Cancelled.")
        return ConversationHandler.END