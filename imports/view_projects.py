from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

from imports.bits import view_projects
from imports import globals

TOKEN = '1544769823:AAHU5H9ycnb9Wad9wCFgRVCh7CPoLW_i72s'
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)


def view_project(update: Update, context: CallbackContext) -> int:
    if len(context.bot_data["projects"]) == 0:
        update.message.reply_text("Sorry, there are no projects at the moment!")
        return ConversationHandler.END
    else:
        keyboard = list()
        for each in context.bot_data["projects"]:
            project = InlineKeyboardButton(each[0], callback_data=each[0])
            keyboard.append([project])

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('To view more details of each project, click on the title.',
                                  reply_markup=reply_markup)

    return globals.VIEW_PROJECTS


def view_project_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == "return":
        keyboard = list()
        for each in context.bot_data["projects"]:
            project = InlineKeyboardButton(each[0], callback_data=each[0])
            keyboard.append([project])

        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text('To view more details of each project, click on the title.',
                                reply_markup=reply_markup)

    for each in context.bot_data["projects"]:
        if query.data == each[0]:
            keyboard = [[InlineKeyboardButton("Join Project", callback_data="join" + each[0])],
                        [InlineKeyboardButton("Go back", callback_data="return")]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            query.edit_message_text(view_projects(each),
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=reply_markup)

        if query.data == "join" + each[0]:
            HAORON = 255414224
            CS = 229599548
            NOAH = 262240949
            username = query.from_user.username.replace("_", "\_")
            bot.sendMessage(chat_id=CS,
                            text=f"Hi, @{username} has signed up for the following project.\n\n"
                                 f"{view_projects(each)}",
                            parse_mode=ParseMode.HTML)
            bot.sendMessage(chat_id=NOAH,
                            text=f"Hi, @{username} has signed up for the following project.\n\n"
                                 f"{view_projects(each)}",
                            parse_mode=ParseMode.HTML)

            query.edit_message_text("Thank you for signing up!\n"
                                    "Your interest has been noted and we will be getting back to you shortly.")

            each[9].append(query.from_user.username)
            return ConversationHandler.END
