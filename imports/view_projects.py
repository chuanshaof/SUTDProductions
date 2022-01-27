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

SOCIALS, VIEW_PROJECTS, SUGGEST = range(3)


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

        keyboard.append([InlineKeyboardButton("Main Menu", callback_data="main")])

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

        keyboard.append([InlineKeyboardButton("Main Menu", callback_data="main")])

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
                NOAH = 262240949
                bot.sendMessage(chat_id=NOAH,
                                text=f"Hi, @{query.from_user.username} has signed up for the following project.\n\n"
                                     f"{view_projects(projects[each])}",
                                parse_mode=ParseMode.HTML)

                query.edit_message_text("Thank you for signing up!\n"
                                        "Your interest has been noted and we will be getting back to you shortly.")
                return ConversationHandler.END


        if query.data == "main":
            keyboard = [[InlineKeyboardButton("Suggest Project", callback_data=str(SUGGEST))],
                        [InlineKeyboardButton("Join our telegram chat", url='https://t.me/joinchat/SME7jUkjNIcSKc9v')],
                        [InlineKeyboardButton("Socials", callback_data=str(SOCIALS))],
                        [InlineKeyboardButton("View Projects", callback_data=str(VIEW_PROJECTS))]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            query.edit_message_text(text=f"Hello <b>{query.from_user.username}</b> and welcome to "
                                         f"<b>SUTD Productions'</b> Video Project Telegram Bot! 👋\n\n"

                                         f"This bot is a one-stop platform for you to share your wildest video ideas, "
                                         f"or to join a team with others. Once enough people have opted into your idea, "
                                         f"we will contact you via Telegram to begin. Ideate - find a team - get filming! 🎬\n\n"

                                         f"We're excited to have you here! We'll be updating the Bot with project ideas "
                                         f"as soon as they're received, so sit tight and get ready to make some videos! 🎥\n\n"

                                         f"The available commands on this bot are:\n"
                                         f"/start - Connect with us\n"
                                         f"/subscribe - Subscribe to the telegram bot for notifications\n"
                                         f"/viewprojects - View and join current projects\n\n"

                                         f"<b>Before you go, remember to:</b>\n"
                                         f"📺 Subscribe to our <a href='https://www.youtube.com/user/SUTDProductions'>YouTube</a> channel\n"
                                         f"📱 Invite your friends to our <a href='https://t.me/joinchat/SME7jUkjNIcSKc9v'>Telegram</a> community\n"
                                         f"📷 Follow us on <a href='https://www.instagram.com/sutdproductions/'>Instagram</a>\n\n"

                                         "Feel free to contact us directly at productions@club.sutd.edu.sg for any "
                                         "questions or feedback!",
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=reply_markup)
