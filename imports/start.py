from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

from imports import globals

SOCIALS = range(1)

TOKEN = '1544769823:AAHU5H9ycnb9Wad9wCFgRVCh7CPoLW_i72s'
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)


# User Interface
# ---------------------------------------------------------------------------------------------#
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Suggest Project", url='https://forms.gle/gQppNaaFqKkCHhHw6')],
                [InlineKeyboardButton("Join our telegram chat", url='https://t.me/joinchat/SME7jUkjNIcSKc9v')],
                [InlineKeyboardButton("Socials", callback_data=str(SOCIALS))]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text=f"Hello <b>{update.message.from_user.username}</b> and welcome to "
                         f"<b>>SUTD Productions'</b> Video Project Telegram Bot! 👋\n\n"

                         f"This bot is a one-stop platform for you to share your wildest video ideas, "
                         f"or to join a team with others. Once enough people have opted into your idea, "
                         f"we will contact you via Telegram to begin. Ideate - find a team - get filming! 🎬\n\n"

                         f"We're excited to have you here! We'll be updating the Bot with project ideas "
                         f"as soon as they're received, so sit tight and get ready to make some videos! 🎥\n\n"

                         f"The available commands on this bot are:\n\n"
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

    return globals.START


# Start QueryHandler
def start_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # Social media list
    if query.data == str(SOCIALS):
        keyboard = [[InlineKeyboardButton("Instagram", url='https://www.instagram.com/sutdproductions/')],
                    [InlineKeyboardButton("Website", url='https://sutd.productions')],
                    [InlineKeyboardButton("Youtube", url='https://www.youtube.com/user/SUTDProductions')],
                    [InlineKeyboardButton("Go Back", callback_data="return")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"Connect with us via the various social medias!", reply_markup=reply_markup)
        return ConversationHandler.END

    elif query.data == "return":
        keyboard = [[InlineKeyboardButton("Suggest Project", url='https://forms.gle/gQppNaaFqKkCHhHw6')],
                    [InlineKeyboardButton("Join our telegram chat", url='https://t.me/joinchat/SME7jUkjNIcSKc9v')],
                    [InlineKeyboardButton("Socials", callback_data=str(SOCIALS))]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.sendMessage(chat_id=update.message.chat_id,
                        text=f"Hello <b>{update.message.from_user.username}</b> and welcome to "
                             f"<b>>SUTD Productions'</b> Video Project Telegram Bot! 👋\n\n"

                             f"This bot is a one-stop platform for you to share your wildest video ideas, "
                             f"or to join a team with others. Once enough people have opted into your idea, "
                             f"we will contact you via Telegram to begin. Ideate - find a team - get filming! 🎬\n\n"

                             f"We're excited to have you here! We'll be updating the Bot with project ideas "
                             f"as soon as they're received, so sit tight and get ready to make some videos! 🎥\n\n"

                             f"The available commands on this bot are:\n\n"
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
