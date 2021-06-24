from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

TOKEN = '1544769823:AAEKdAMDlPKuxL30_QuHmM8Am1OZoNep24s'
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

EDIT, EDIT_CONFIRM = range(2)

# Editing projects
# ---------------------------------------------------------------------------------------------#
def edit(update: Update, context: CallbackContext) -> None:
    if "admin" not in context.bot_data:
        context.bot_data["admin"] = list()
        return

    if update.message.from_user.id not in context.bot_data["admin"]:
        return

    if len(context.bot_data["projects"]) == 0:
        update.message.reply_text("Sorry, there are no projects at the moment!")
        return

    projects = format_project_list(update, context)
    keyboard = list()
    for each in projects:
        project = InlineKeyboardButton(each, callback_data=each)
        keyboard.append([project])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Click on the title of the project you would like to edit.',
                              reply_markup=reply_markup)
    return EDIT


# Remove project (CONFIRM)
def edit_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    global temp_edit
    temp_edit = query.data

    if query.data == "return":
        projects = format_project_list(update, context)
        keyboard = list()
        for each in projects:
            project = InlineKeyboardButton(each, callback_data=each)
            keyboard.append([project])

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('Click on the title of the project you would like to edit.',
                                reply_markup=reply_markup)

    # Each here is the list of items
    for each in context.bot_data["projects"]:
        if query.data == each[0]:
            keyboard = [[InlineKeyboardButton("Name", callback_data="name" + each[0]),
                         InlineKeyboardButton("Description", callback_data="description" + each[0])],
                        [InlineKeyboardButton("POC", callback_data="poc" + each[0]),
                         InlineKeyboardButton("Venue", callback_data="venue" + each[0])],
                        [InlineKeyboardButton("Partners", callback_data="partners" + each[0]),
                         InlineKeyboardButton("Inspiration", callback_data="inspiration" + each[0])],
                        [InlineKeyboardButton("Roles", callback_data="roles" + each[0]),
                         InlineKeyboardButton("Deadline", callback_data="deadline" + each[0])],
                        [InlineKeyboardButton("Requirements", callback_data="requirements" + each[0]),
                         InlineKeyboardButton("Team", callback_data="team" + each[0])],
                        [InlineKeyboardButton("Go Back", callback_data="return")]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            query.edit_message_text(f"*Click on the details that you would like to edit.*\n\n"
                                    f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=reply_markup)

        elif query.data == "name" + each[0]:
            query.edit_message_text(f"Enter the new project name.",
                                    parse_mode=ParseMode.MARKDOWN)
            return EDIT_CONFIRM

        elif query.data == "description" + each[0]:
            query.edit_message_text(f"Enter the new project description.",
                                    parse_mode=ParseMode.MARKDOWN)
            return EDIT_CONFIRM

        elif query.data == "poc" + each[0]:
            query.edit_message_text(f"Enter the new project POC.",
                                    parse_mode=ParseMode.MARKDOWN)
            return EDIT_CONFIRM

        elif query.data == "venue" + each[0]:
            query.edit_message_text(f"Enter the new project venue.",
                                    parse_mode=ParseMode.MARKDOWN)
            return EDIT_CONFIRM

        elif query.data == "partners" + each[0]:
            query.edit_message_text(f"Enter the new project partners.",
                                    parse_mode=ParseMode.MARKDOWN)
            return EDIT_CONFIRM

        elif query.data == "inspiration" + each[0]:
            query.edit_message_text(f"Enter the new project inspiration.",
                                    parse_mode=ParseMode.MARKDOWN)
            return EDIT_CONFIRM

        elif query.data == "roles" + each[0]:
            query.edit_message_text(f"Enter the new project required roles.",
                                    parse_mode=ParseMode.MARKDOWN)
            return EDIT_CONFIRM

        elif query.data == "deadline" + each[0]:
            query.edit_message_text(f"Enter the new project deadline.",
                                    parse_mode=ParseMode.MARKDOWN)
            return EDIT_CONFIRM

        elif query.data == "requirements" + each[0]:
            query.edit_message_text(f"Enter the new project requirements.",
                                    parse_mode=ParseMode.MARKDOWN)
            return EDIT_CONFIRM

        elif query.data == "team" + each[0]:
            query.edit_message_text(f"Enter the new project team.",
                                    parse_mode=ParseMode.MARKDOWN)
            return EDIT_CONFIRM

        elif "confirm" + "name" + each[0] in query.data:
            length = len("confirm" + "name" + each[0])
            each[0] = query.data[length:]
            query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                         f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END

        elif "confirm" + "description" + each[0] in query.data:
            length = len("confirm" + "description" + each[0])
            each[1] = query.data[length:]
            query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                         f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END

        elif "confirm" + "poc" + each[0] in query.data:
            length = len("confirm" + "poc" + each[0])
            each[2] = query.data[length:]
            query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                         f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END

        elif "confirm" + "venue" + each[0] in query.data:
            length = len("confirm" + "venue" + each[0])
            each[3] = query.data[length:]
            query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                         f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END

        elif "confirm" + "partners" + each[0] in query.data:
            length = len("confirm" + "partners" + each[0])
            each[4] = query.data[length:]
            query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                         f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END

        elif "confirm" + "inspiration" + each[0] in query.data:
            length = len("confirm" + "inspiration" + each[0])
            each[5] = query.data[length:]
            query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                         f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END

        elif "confirm" + "roles" + each[0] in query.data:
            length = len("confirm" + "roles" + each[0])
            each[6] = query.data[length:]
            query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                         f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END

        elif "confirm" + "deadline" + each[0] in query.data:
            length = len("confirm" + "deadline" + each[0])
            each[7] = query.data[length:]
            query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                         f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END

        elif "confirm" + "requirements" + each[0] in query.data:
            length = len("confirm" + "requirements" + each[0])
            each[8] = query.data[length:]
            query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                         f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END

        elif "confirm" + "team" + each[0] in query.data:
            length = len("confirm" + "team" + each[0])
            each[9] = query.data[length:]
            query.edit_message_text(text=f"Project details have been updated as accordingly.\n\n"
                                         f"{view_projects(each)}",
                                    parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END


# Editing confirmation
def edit_confirmation(update: Update, context: CallbackContext) -> None:
    # Each here is the list of items
    for each in context.bot_data["projects"]:
        keyboard = [[InlineKeyboardButton("Confirm Edit", callback_data="confirm" + temp_edit + update.message.text)],
                    [InlineKeyboardButton("Go Back", callback_data=each[0])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        temp_proj = each.copy()

        if temp_edit == "name" + each[0]:
            temp_proj[0] = update.message.text
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=f"{view_projects(temp_proj)}",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)

        elif temp_edit == "description" + each[0]:
            temp_proj[1] = update.message.text
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=f"{view_projects(temp_proj)}",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)

        elif temp_edit == "poc" + each[0]:
            temp_proj[2] = update.message.text
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=f"{view_projects(temp_proj)}",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)

        elif temp_edit == "venue" + each[0]:
            temp_proj[3] = update.message.text
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=f"{view_projects(temp_proj)}",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)

        elif temp_edit == "partners" + each[0]:
            temp_proj[4] = update.message.text
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=f"{view_projects(temp_proj)}",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)

        elif temp_edit == "inspiration" + each[0]:
            temp_proj[5] = update.message.text
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=f"{view_projects(temp_proj)}",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)

        elif temp_edit == "roles" + each[0]:
            temp_proj[6] = update.message.text
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=f"{view_projects(temp_proj)}",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)

        elif temp_edit == "deadline" + each[0]:
            temp_proj[7] = update.message.text
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=f"{view_projects(temp_proj)}",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)

        elif temp_edit == "requirements" + each[0]:
            temp_proj[8] = update.message.text
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=f"{view_projects(temp_proj)}",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)

        elif temp_edit == "team" + each[0]:
            temp_proj[9] = update.message.text
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=f"{view_projects(temp_proj)}",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    return EDIT


# Returns a list, used in multiple places
def format_project_list(update: Update, context: CallbackContext) -> list:
    if "projects" not in context.bot_data:
        context.bot_data["projects"] = list()
        return list()
    list_of_names = list()
    for each in context.bot_data["projects"]:
        list_of_names.append(each[0])
    return list_of_names


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