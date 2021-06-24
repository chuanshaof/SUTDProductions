from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

from imports import bits, subscribe, remove, edit, admin, announce, add, start, view_projects

import logging

import os

"""
git add .
git commit -m "changing python3 to python in Procfile"
git push heroku master
"""

WAIT_CODE = range(1)
START = range(1)
PROJECT_NAME, PROJECT_DESCRIPTION, PROJECT_POC, PROJECT_VENUE, PROJECT_PARTNERS, PROJECT_INSPIRATION, \
PROJECT_ROLES, PROJECT_DEADLINE, PROJECT_REQUIREMENTS, PROJECT_TEAM, PROJECT_CONFIRM = range(11)
REMOVE = range(1)
ANNOUNCE_QUERY, ANNOUNCE = range(2)
EDIT, EDIT_CONFIRM = range(2)
VIEW_PROJECTS = range(1)

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
my_persistence = PicklePersistence(filename='my_file')

TOKEN = '1544769823:AAEKdAMDlPKuxL30_QuHmM8Am1OZoNep24s'
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, persistence=my_persistence, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("clear_admins", bits.clear_admins))
    dp.add_handler(CommandHandler("check_subs", bits.check_subs))
    dp.add_handler(CommandHandler("subscribe", subscribe.subscribe))

    # Start handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("start", start.start)
        ],
        states={
            START: [CallbackQueryHandler(start.start_query)]
        },
        fallbacks=[MessageHandler(Filters.command, cancel)],
        allow_reentry=True
    ))

    # Remove handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("remove", remove.remove)
        ],
        states={
            REMOVE: [CallbackQueryHandler(remove.remove_confirm)]
        },
        fallbacks=[MessageHandler(Filters.command, cancel)]
    ))

    # Edit handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("edit", edit.edit)
        ],
        states={
            EDIT: [CallbackQueryHandler(edit.edit_query)],
            EDIT_CONFIRM: [CallbackQueryHandler(edit.edit_confirmation)]
        },
        fallbacks=[MessageHandler(Filters.command, cancel)],
        allow_reentry=True
    ))

    # Admin handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("admin", admin.admin)
        ],
        states={
            WAIT_CODE: [MessageHandler(Filters.text, admin.verify)]
        },
        fallbacks=[MessageHandler(Filters.command, cancel)]
    ))

    # Adding project
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("add", add.add)
        ],
        states={
            PROJECT_NAME: [MessageHandler(Filters.text & (~ Filters.command), add.project_name)],
            PROJECT_DESCRIPTION: [MessageHandler(Filters.text & (~ Filters.command), add.project_description)],
            PROJECT_POC: [MessageHandler(Filters.text & (~ Filters.command), add.project_poc)],
            PROJECT_VENUE: [MessageHandler(Filters.text & (~ Filters.command), add.project_venue)],
            PROJECT_PARTNERS: [MessageHandler(Filters.text & (~ Filters.command), add.project_partners)],
            PROJECT_INSPIRATION: [MessageHandler(Filters.text & (~ Filters.command), add.project_inspiration)],
            PROJECT_ROLES: [MessageHandler(Filters.text & (~ Filters.command), add.project_roles)],
            PROJECT_DEADLINE: [MessageHandler(Filters.text & (~ Filters.command), add.project_deadline)],
            PROJECT_REQUIREMENTS: [MessageHandler(Filters.text & (~ Filters.command), add.project_requirement)],
            PROJECT_TEAM: [MessageHandler(Filters.text & (~ Filters.command), add.project_team)],
            PROJECT_CONFIRM: [CallbackQueryHandler(add.project_confirm)]
        },
        fallbacks=[MessageHandler(Filters.command, cancel)],
        allow_reentry=True
    ))

    # Announce handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("announce", announce.announce)
        ],
        states={
            ANNOUNCE_QUERY: [MessageHandler(Filters.all & (~ Filters.command), announce.announcement_confirm)],
            ANNOUNCE: [CallbackQueryHandler(announce.announcement)]
        },
        fallbacks=[MessageHandler(Filters.command, cancel)],
        allow_reentry=True
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("view_projects", view_projects.view_project)
        ],
        states={
            VIEW_PROJECTS: [CallbackQueryHandler(view_projects.view_project_query)]
        },
        fallbacks=[MessageHandler(Filters.command, cancel)],
        allow_reentry=True
    ))

    # log all errors
    dp.add_error_handler(error)

    updater.start_polling()

    # # Start the Bot
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook('https://boiling-badlands-67618.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


# Cancel action
def cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Action cancelled.")
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    main()
