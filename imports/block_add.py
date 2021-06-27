from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

import os

from imports.bits import view_projects
from imports import globals

TOKEN = os.environ["API_KEY"]
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)


# Adding Projects
# ---------------------------------------------------------------------------------------------#
def block_add(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(f"Please enter the new project details in the format of:\n\n"
                              f"<b>[Project Name]</b>\n" \
                              f"<i>[Project Details]</i>\n" \
                              f"POC: \n" \
                              f"Venue: \n" \
                              f"Project Purpose: \n" \
                              f"Inspiration: \n" \
                              f"Roles needed: \n" \
                              f"Production Deadline: \n" \
                              f"Project Requirement: \n" \
                              f"Team: \n",
                              parse_mode=ParseMode.HTML)
    print("test")
