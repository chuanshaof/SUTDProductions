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


# Returns a formatted string, used in multiple places
def view_projects(project: list) -> str:
    view_proj = f"<b>{project[0]}</b>\n" \
                f"<i>{project[1]}</i>\n" \
                f"POC: {project[2]}\n" \
                f"Venue: {project[3]}\n" \
                f"Project Purpose: {project[4]}\n" \
                f"Inspiration: {project[5]}\n" \
                f"Roles needed: {project[6]}\n" \
                f"Production Deadline: {project[7]}\n" \
                f"Project Requirement: {project[8]}\n" \
                f"Team: {project[9]}\n"
    return view_proj
