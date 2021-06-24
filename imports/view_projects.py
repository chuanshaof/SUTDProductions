from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

TOKEN = '1544769823:AAEKdAMDlPKuxL30_QuHmM8Am1OZoNep24s'
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

VIEW_PROJECTS = range(1)


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

    return VIEW_PROJECTS


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
                                    parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=reply_markup)

        if query.data == "join" + each[0]:
            HAORON = 255414224
            CS = 229599548
            bot.sendMessage(chat_id=CS,
                            text=f"Hi Haoron, @{query.from_user.username} has signed up for the following project.\n\n"
                                 f"{view_projects(each)}",
                            parse_mode=ParseMode.MARKDOWN)

            query.edit_message_text("Thank you for signing up!\n"
                                    "Your interest has been indicated and we will be getting back to you shortly.")
            return ConversationHandler.END


# Returns a formatted string, used in multiple places
def view_projects(project: list) -> str:
    view_proj = f"*{project[0]}*\n" \
                f"_{project[1]}_\n" \
                f"POC: @{project[2]}\n" \
                f"Venue: {project[3]}\n" \
                f"Partners: {project[4]}\n" \
                f"Inspiration: [{project[5]}]({project[5]})\n" \
                f"Roles needed: {project[6]}\n" \
                f"Production Deadline: {project[7]}\n" \
                f"Project Requirement: {project[8]}\n" \
                f"Team: {project[9]}\n"
    return view_proj
