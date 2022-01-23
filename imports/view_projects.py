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


def view_project(update: Update, context: CallbackContext) -> int:
    projects = firebase.db.child("project").get().val()

    if projects == None:
        update.message.reply_text("Sorry, there are no projects at the moment!")
        return ConversationHandler.END
    else:
        keyboard = list()
        for each in projects:
            project = InlineKeyboardButton(each, callback_data=each)
            keyboard.append([project])

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('To view more details of each project, click on the title.',
                                  reply_markup=reply_markup)
        return globals.VIEW_PROJECTS


def view_project_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    projects = firebase.db.child("project").get().val()

    if query.data == "return":
        keyboard = list()
        for each in projects:
            project = InlineKeyboardButton(each, callback_data=each)
            keyboard.append([project])

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('To view more details of each project, click on the title.',
                                reply_markup=reply_markup)

    for each in projects:
        if query.data == each:
            keyboard = [[InlineKeyboardButton("Join Project", callback_data="join" + each)],
                        [InlineKeyboardButton("Go back", callback_data="return")]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            query.edit_message_text(view_projects(projects[each]),
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=reply_markup)

        if query.data == "join" + each:
            if query.from_user.username in projects[each][9]:
                query.edit_message_text(f"You have already signed up for this project, "
                                        f"please contact @{globals.PRESIDENT} to check your join status.")
                return ConversationHandler.END
            else:
                # projects[each][9] = projects[each][9] + "\n@" + query.from_user.username
                CS = 229599548
                NOAH = 262240949
                bot.sendMessage(chat_id=NOAH,
                                text=f"Hi, @{query.from_user.username} has signed up for the following project.\n\n"
                                     f"{view_projects(projects[each])}",
                                parse_mode=ParseMode.HTML)
                bot.sendMessage(chat_id=CS,
                                text=f"Hi, @{query.from_user.username} has signed up for the following project.\n\n"
                                     f"{view_projects(projects[each])}",
                                parse_mode=ParseMode.HTML)

                # firebase.db.child("project")\
                #     .child(each)\
                #     .set(projects[each])

                query.edit_message_text("Thank you for signing up!\n"
                                        "Your interest has been noted and we will be getting back to you shortly.")
                return ConversationHandler.END
