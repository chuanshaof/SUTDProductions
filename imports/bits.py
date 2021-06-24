from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence


# Check subscribed members
def check_subs(update: Update, context: CallbackContext) -> None:
    subs = ""
    for each in context.bot_data["subscribe"]:
        subs = subs + "@" + each[1] + "\n"
    update.message.reply_text(subs)
    return


# ---------------------------------------------------------------------------------------------#
# Clearing of admins
def clear_admins(update: Update, context: CallbackContext) -> None:
    if "admin" not in context.bot_data:
        context.bot_data["admin"] = list()

    if update.message.from_user.id not in context.bot_data["admin"]:
        return
    else:
        context.bot_data["admin"].clear()
        update.message.reply_text("Admin list cleared.")