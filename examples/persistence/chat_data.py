from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler

from itertools import zip_longest


def greet(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if "users_talked_to" not in context.bot_data:
        context.bot_data["users_talked_to"] = set()
    context.bot_data["users_talked_to"].add(user_id)
    num_people = len(context.bot_data["users_talked_to"])
    update.message.reply_text(f"Hello! A total of {num_people} people have spoken to this bot.")


def pat(update: Update, context: CallbackContext) -> None:
    if "times_patted" not in context.chat_data:
        context.chat_data["times_patted"] = 0
    context.chat_data["times_patted"] += 1
    times_patted = context.chat_data["times_patted"]
    update.message.reply_text(f"This dog has been patted {times_patted} times")


def new_item(update: Update, context: CallbackContext) -> None:
    if "entries" not in context.user_data:
        context.user_data["entries"] = list()
    context.user_data["entries"].append(" ".join(context.args))
    num_items = len(context.user_data["entries"])
    update.message.reply_text(f"Item added! You now have {num_items} items in your shopping list")


def list_items(update: Update, context: CallbackContext) -> None:
    if "entries" not in context.user_data:
        context.user_data["entries"] = list()
    num_items = len(context.user_data["entries"])
    shopping_list = "\n".join([f"- {item}" for item in context.user_data["entries"]])
    update.message.reply_text(f"You have {num_items} items in your shopping list: \n\n{shopping_list}")


updater = Updater('1513453891:AAEJ2C2Qhbcp2-oQztsdR-3EFzfN-Cgqax0')

# updater.dispatcher.add_handler(MessageHandler(Filters.text & (~ Filters.forwarded), greet))
# updater.dispatcher.add_handler(CommandHandler("pat", pat))
updater.dispatcher.add_handler(CommandHandler("add", new_item))
updater.dispatcher.add_handler(CommandHandler("list", list_items))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    updater.start_polling()
    updater.idle()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
