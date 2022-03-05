from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

from imports import bits, subscribe, remove, edit, admin, announce, start, globals, add, suggest

import firebase
import logging
import os

"""
git add .
git commit -m "changing python3 to python in Procfile"
git push heroku Head:master
git push heroku master
"""

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.environ["API_KEY"]
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # States
    edit_states = {
        globals.EDIT:
            [CallbackQueryHandler(edit.edit_query)],
        globals.EDIT_CONFIRM:
            [MessageHandler(Filters.text & (~ Filters.command), edit.edit_confirmation)]
    }

    announce_states = {
        globals.ANNOUNCE_QUERY:
            [MessageHandler(Filters.all & (~ Filters.command), announce.announcement_confirm)],
        globals.ANNOUNCE:
            [CallbackQueryHandler(announce.announcement)]
    }

    admin_states = {
        globals.WAIT_CODE:
            [MessageHandler(Filters.text & (~ Filters.command), admin.verify)]
    }

    add_states = {
        globals.ADD:
            [MessageHandler(Filters.text & (~ Filters.command), add.confirm)],
        globals.PROJECT_CONFIRM:
            [CallbackQueryHandler(add.project_confirm)]
    }

    suggest_states = {
        globals.SUGGEST:
            [MessageHandler(Filters.text & (~ Filters.command), suggest.confirm)],
        globals.SUGGEST_CONFIRM:
            [CallbackQueryHandler(suggest.project_confirm)]
    }

    state_1 = {**edit_states, **announce_states, **admin_states, **add_states, **suggest_states}

    state_2 = {
            globals.START: [CallbackQueryHandler(start.start_query)],
            globals.REMOVE: [CallbackQueryHandler(remove.remove_confirm)]
        }

    all_states = {**state_1, **state_2}

    # Start handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("start", start.start),
            CommandHandler("subscribe", subscribe.subscribe),
            CommandHandler("check_subs", bits.check_subs),
            CommandHandler("clear_admins", bits.clear_admins),
            CommandHandler("viewprojects", start.view_project),
            CommandHandler("remove", remove.remove),
            CommandHandler("admin", admin.admin),
            CommandHandler("edit", edit.edit),
            CommandHandler("announce", announce.announce),
            CommandHandler("add", add.add),
            CommandHandler("suggest", suggest.suggest)
        ],
        states=all_states,
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    ))

    # log all errors
    dp.add_error_handler(error)

    # updater.start_polling()

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://sutdproductions.herokuapp.com/' + TOKEN)

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
    firebase.initialize()
    globals.initialize()
    main()
