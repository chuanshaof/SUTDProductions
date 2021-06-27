from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

import os

from imports.bits import view_projects
from imports import globals

TOKEN = os.environ["API_KEY"]
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

project_details = ["name",
                   "description",
                   "POC",
                   "venue",
                   "purpose",
                   "inspiration",
                   "roles",
                   "deadline",
                   "requirements",
                   "team"]


# Editing projects
# ---------------------------------------------------------------------------------------------#
def edit(update: Update, context: CallbackContext) -> None:
    if "admin" not in context.bot_data:
        context.bot_data["admin"] = list()
        return

    context.user_data["temp_edit"] = str()

    if update.message.from_user.id not in context.bot_data["admin"]:
        return

    if len(context.bot_data["projects"]) == 0:
        update.message.reply_text("Sorry, there are no projects at the moment!")
        return

    keyboard = list()
    for each in context.bot_data["projects"]:
        project = InlineKeyboardButton(each[0], callback_data=each[0])
        keyboard.append([project])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('<b>Click on the title of the project you would like to edit.</b>',
                              parse_mode=ParseMode.HTML,
                              reply_markup=reply_markup)
    return globals.EDIT


# Remove project (CONFIRM)
def edit_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    global temp_edit
    temp_edit = query.data

    if query.data == "return":
        keyboard = list()
        for each in context.bot_data["projects]"]:
            project = InlineKeyboardButton(each[0], callback_data=each[0])
            keyboard.append([project])

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('Click on the title of the project you would like to edit.',
                                reply_markup=reply_markup)

    # Each here is the list of items
    for each in context.bot_data["projects"]:
        if query.data == each[0]:
            context.user_data["temp_edit"] = each[0]

            keyboard = [[InlineKeyboardButton("Name", callback_data=project_details[0]),
                         InlineKeyboardButton("Description", callback_data=project_details[1])],
                        [InlineKeyboardButton("POC", callback_data=project_details[2]),
                         InlineKeyboardButton("Venue", callback_data=project_details[3])],
                        [InlineKeyboardButton("Purpose", callback_data=project_details[4]),
                         InlineKeyboardButton("Inspiration", callback_data=project_details[5])],
                        [InlineKeyboardButton("Roles", callback_data=project_details[6]),
                         InlineKeyboardButton("Deadline", callback_data=project_details[7])],
                        [InlineKeyboardButton("Requirements", callback_data=project_details[8]),
                         InlineKeyboardButton("Team", callback_data=project_details[9])],
                        [InlineKeyboardButton("Go Back", callback_data="return")]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            query.edit_message_text(f"<b>Click on the details that you would like to edit.</b>\n\n"
                                    f"{view_projects(each)}",
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=reply_markup)
        else:
            for every in range(len(project_details)):
                if query.data == project_details[every] and context.user_data["temp_edit"] == each[0]:
                    query.edit_message_text(f"Current project {project_details[every]}:\n"
                                            f"{each[every]}\n\n"
                                            f"Enter the new project {project_details[every]}.",
                                            parse_mode=ParseMode.HTML)
                    context.user_data["temp_edit"] = project_details[every] + each[0]
                    return globals.EDIT_CONFIRM

                elif query.data == "confirm":
                    if project_details[every] + each[0] in context.user_data["temp_edit"]:
                        length = len(project_details[every] + each[0])
                        each[every] = context.user_data["temp_edit"][length:]
                        query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                                     f"{view_projects(each)}",
                                                     parse_mode=ParseMode.HTML)
                        return ConversationHandler.END


# Editing confirmation
def edit_confirmation(update: Update, context: CallbackContext) -> None:
    # Each here is the list of items
    for each in context.bot_data["projects"]:
        keyboard = [[InlineKeyboardButton("Confirm Edit", callback_data="confirm")],
                    [InlineKeyboardButton("Go Back", callback_data=each[0])]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        temp_proj = each.copy()

        for every in range(len(project_details)):
            if context.user_data["temp_edit"] == project_details[every] + each[0]:
                if every == 1:
                    if len(update.message.text) > 50:
                        update.message.reply_text("Please enter project name, maximum of 50 characters all in one line.")
                        return globals.EDIT_CONFIRM

                    for blah in context.bot_data["projects"]:
                        if update.message.text == blah[0]:
                            update.message.reply_text("Project name has been taken, please key in a new project name.")
                            return globals.EDIT_CONFIRM
                    else:
                        context.user_data["temp_edit"] = project_details[every] + each[0] + update.message.text
                        temp_proj[every] = update.message.text
                        bot.sendMessage(chat_id=update.message.chat_id,
                                        text=f"Please confirm the new project details:\n\n"
                                             f"{view_projects(temp_proj)}",
                                        parse_mode=ParseMode.HTML,
                                        reply_markup=reply_markup)
                        return globals.EDIT
                else:
                    context.user_data["temp_edit"] = project_details[every] + each[0] + update.message.text
                    temp_proj[every] = update.message.text
                    bot.sendMessage(chat_id=update.message.chat_id,
                                    text=f"Please confirm the new project details:\n\n"
                                         f"{view_projects(temp_proj)}",
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=reply_markup)
                    return globals.EDIT
