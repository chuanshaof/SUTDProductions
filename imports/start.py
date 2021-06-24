from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

START = range(1)
SOCIALS = range(1)

TOKEN = '1544769823:AAEKdAMDlPKuxL30_QuHmM8Am1OZoNep24s'
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
                    text=f"Hello *{update.message.from_user.username}* and welcome to *SUTD Productions'* "
                         f"Video Project Telegram Bot! 👋\n\n"

                         f"This bot is a one-stop platform for you to share your wildest video ideas, "
                         f"or to join a team with others. Once enough people have opted into your idea, "
                         f"we will contact you via Telegram to begin. Ideate - find a team - get filming! 🎬\n\n"

                         f"We're excited to have you here! We'll be updating the Bot with project ideas "
                         f"as soon as they're received, so sit tight and get ready to make some videos! 🎥\n\n"

                         f"*Before you go, remember to:*\n"
                         f"📺 Subscribe to our [YouTube](https://www.youtube.com/user/SUTDProductions) channel\n"
                         f"📱 Invite your friends to our [Telegram](https://t.me/joinchat/SME7jUkjNIcSKc9v) community\n"
                         f"📷 Follow us on [Instagram](https://www.instagram.com/sutdproductions/)\n\n"

                         "Feel free to contact us directly at productions@club.sutd.edu.sg for any "
                         "questions or feedback!",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup)

    return START


# Start QueryHandler
def start_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # Social media list
    if query.data == str(SOCIALS):
        keyboard = [[InlineKeyboardButton("Instagram", url='https://www.instagram.com/sutdproductions/')],
                    [InlineKeyboardButton("Website", url='https://sutd.productions')],
                    [InlineKeyboardButton("Youtube", url='https://www.youtube.com/user/SUTDProductions')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"Connect with us via the various social medias!", reply_markup=reply_markup)
        return ConversationHandler.END