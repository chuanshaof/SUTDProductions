from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

import os

from imports.bits import view_projects
from imports import globals
import firebase

SOCIALS, VIEW_PROJECTS, SUGGEST = range(3)

TOKEN = os.environ["API_KEY"]
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

start_keyboard = [[InlineKeyboardButton("Join our telegram chat", url='https://t.me/joinchat/SME7jUkjNIcSKc9v')],
                  [InlineKeyboardButton("Suggest Project", callback_data=str(SUGGEST))],
                  [InlineKeyboardButton("Socials", callback_data=str(SOCIALS))],
                  [InlineKeyboardButton("View Projects", callback_data=str(VIEW_PROJECTS))]]


# User Interface
# ---------------------------------------------------------------------------------------------#
def start(update: Update, context: CallbackContext) -> None:
    reply_markup = InlineKeyboardMarkup(start_keyboard)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text=f"Hello <b>{update.message.from_user.username}</b> and welcome to "
                         f"SUTD Productions' <b>Video Project Telegram Bot!</b> 👋\n\n"

                         f"This bot is a one-stop platform for you to share your wildest video project ideas "
                         f"and connect with other people to produce them. You can also view other people's ideas, "
                         f"and join their production team. Once enough people have opted into your idea, "
                         f"we will contact you via Telegram to begin. "
                         f"<b>Ideate - find a team - get filming!</b> 🎬\n\n"

                         f"We're excited to have you here! We'll be updating the Bot with project ideas "
                         f"as soon as they're received, so sit tight and get ready to make some videos! 🎥\n\n"

                         f"<b>Before you go, remember to:</b>\n"
                         f"📺 Subscribe to our <a href='https://www.youtube.com/user/SUTDProductions'>YouTube</a> channel\n"
                         f"📱 Invite your friends to our <a href='https://t.me/joinchat/SME7jUkjNIcSKc9v'>Telegram</a> community\n"
                         f"📷 Follow us on <a href='https://www.instagram.com/sutdproductions/'>Instagram</a>\n\n"

                         "Any questions or feedback can be directed to @kong_noah.",
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup)

    return globals.START


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
        return globals.START

# Start QueryHandler
def start_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # This is for Main_Menu
    # -----------------------------------------------------------------------------------------------------------------#
    if query.data == "main":
        reply_markup = InlineKeyboardMarkup(start_keyboard)

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

    # This is for SOCIALS
    # -----------------------------------------------------------------------------------------------------------------#
    if query.data == str(SOCIALS):
        keyboard = [[InlineKeyboardButton("Instagram", url='https://www.instagram.com/sutdproductions/')],
                    [InlineKeyboardButton("Website", url='https://sutd.productions')],
                    [InlineKeyboardButton("Youtube", url='https://www.youtube.com/user/SUTDProductions')],
                    [InlineKeyboardButton("Main Menu", callback_data="main")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"Connect with us via the various social medias!", reply_markup=reply_markup)

    # This is for view_projects
    # -----------------------------------------------------------------------------------------------------------------#
    projects = firebase.db.child("project").get().val()

    if query.data == str(VIEW_PROJECTS):

        if projects == None:
            query.edit_message_text("Sorry, there are no projects at the moment!")
            return ConversationHandler.END
        else:
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
                        [InlineKeyboardButton("Go back", callback_data=str(VIEW_PROJECTS))]]

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

    # This is for suggest_projects
    # -----------------------------------------------------------------------------------------------------------------#
    if query.data == str(SUGGEST):
        text = "Please use /start to return to Main Menu\n\n" \
               "" \
               "Suggest a project in the format of:\n" \
               "(For empty entries, put NIL)\n\n"
        for every in range(len(globals.project_details)):
            text = text + globals.project_details[every] + "\n"

        query.edit_message_text(text,
                                parse_mode=ParseMode.HTML)

        return globals.SUGGEST
