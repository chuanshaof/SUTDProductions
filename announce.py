from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

TOKEN = '1544769823:AAFJK_Md3EV8AMWHJG4i9Qaxe_LhCP6Jb5E'
bot = Bot(TOKEN)

def announce(update: Update, context: CallbackContext) -> None:
    if "admin" not in context.bot_data:
        context.bot_data["admin"] = list()

    if update.message.from_user.id not in context.bot_data["admin"]:
        return
    else:
        if "subscribe" not in context.bot_data:
            context.bot_data["subscribe"] = list()
            update.message.reply_text("No one is subscribed to the bot.")
            return
        elif len(context.bot_data["subscribe"]) == 0:
            update.message.reply_text("No one is subscribed to the bot.")
            return
        else:
            update.message.reply_text("Enter the message to announce.")
            return ANNOUNCE_QUERY


def announcement_confirm(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Confirm", callback_data="Y")],
                [InlineKeyboardButton("Cancel", callback_data="N")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    global announce_message
    announce_message = update.message.text

    bot.sendMessage(chat_id=update.message.chat_id,
                    text=f"Confirm announcement message:\n\n"
                         f"{update.message.text}",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup)
    return ANNOUNCE


def announcement(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == "Y":
        for each in context.bot_data["subscribe"]:
            forward_to = str(each[0])
            bot.sendMessage(chat_id=forward_to,
                            text=announce_message,
                            parse_mode=ParseMode.MARKDOWN)
        query.edit_message_text("Successfully announced to subscribers.")
        return ConversationHandler.END
    elif query.data == "N":
        query.edit_message_text("Cancelled.")
        return ConversationHandler.END