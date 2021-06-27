from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

import os

from imports.bits import view_projects
from imports import globals

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
def block_add(update: Update, context: CallbackContext) -> int:
    text = "Please enter the new project details in the format of:\n\n"
    for every in range(len(add_details)):
        text = text + add_details[every] + "\n"
    update.message.reply_text(text,
                              parse_mode=ParseMode.HTML)

    return globals.BLOCK_ADD


def confirm(update: Update, context: CallbackContext) -> int:
    context.user_data["temp_project"] = list()

    for every in range(len(add_details)):
        if add_details[every] not in update.message.text:
            update.message.reply_text("Project details are incomplete, please use /block_add to retry accordingly "
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
        elif every == 0:
            found = update.message.text.find(add_details[every]) + len(add_details[every])
            next_find = update.message.text.find(add_details[every + 1])
            name = update.message.text[found:next_find-2]

            if not name or len(name) > 50 or "\n" in name:
                update.message.reply_text("Please enter a valid project name.")
                return ConversationHandler.END

            for each in context.bot_data["projects"]:
                if name == each[0]:
                    update.message.reply_text("Project name has been taken, please key in a new project name.")
                    return ConversationHandler.END

            context.user_data["temp_project"].append(update.message.text[found:next_find - 2])

        else:
            found = update.message.text.find(add_details[every]) + len(add_details[every])
            next_find = update.message.text.find(add_details[every + 1])
            context.user_data["temp_project"].append(update.message.text[found:next_find-2])

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
