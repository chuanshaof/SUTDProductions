from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

TOKEN = '1544769823:AAEKdAMDlPKuxL30_QuHmM8Am1OZoNep24s'
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

PROJECT_NAME, PROJECT_DESCRIPTION, PROJECT_POC, PROJECT_VENUE, PROJECT_PARTNERS, PROJECT_INSPIRATION, \
PROJECT_ROLES, PROJECT_DEADLINE, PROJECT_REQUIREMENTS, PROJECT_TEAM, PROJECT_CONFIRM = range(11)

temp_project = list()


# Adding Projects
# ---------------------------------------------------------------------------------------------#
def add(update: Update, context: CallbackContext) -> int:
    if "projects" not in context.bot_data:
        context.bot_data["projects"] = list()

    if update.message.from_user.id not in context.bot_data["admin"]:
        return ConversationHandler.END
    else:
        if "projects" not in context.bot_data:
            context.bot_data["projects"] = list()
        temp_project.clear()
        update.message.reply_text("Please enter project name.")
        return PROJECT_NAME


# Adding Projects (TITLE)
def project_name(update: Update, context: CallbackContext) -> int:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project name.")
        return PROJECT_NAME

    for each in context.bot_data["projects"]:
        if update.message.text == each[0]:
            update.message.reply_text("Project name has been taken, please key in a new project name.")
            return PROJECT_NAME
        else:
            temp_project.append(update.message.text)

    update.message.reply_text("Please enter project description.")
    return PROJECT_DESCRIPTION


# Adding Projects (DETAILS)
def project_description(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project description.")
        return PROJECT_DESCRIPTION
    else:
        temp_project.append(update.message.text)

    update.message.reply_text("Please enter project POC.")

    return PROJECT_POC


# Adding Projects (DETAILS)
def project_poc(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project POC.")
        return PROJECT_POC
    else:
        temp_project.append(update.message.text)

    update.message.reply_text("Please enter project venue.")

    return PROJECT_VENUE


# Adding Projects (DETAILS)
def project_venue(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project venue.")
        return PROJECT_VENUE
    else:
        temp_project.append(update.message.text)

    update.message.reply_text("Please enter project partners.")

    return PROJECT_PARTNERS


# Adding Projects (DETAILS)
def project_partners(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project partner.")
        return PROJECT_PARTNERS
    else:
        temp_project.append(update.message.text)

    update.message.reply_text("Please enter project inspiration.")

    return PROJECT_INSPIRATION


# Adding Projects (INSPIRATION)
def project_inspiration(update: Update, context: CallbackContext) -> int:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project inspiration.")
        return PROJECT_DESCRIPTION
    else:
        temp_project.append(update.message.text)

    update.message.reply_text("Please enter project roles.")
    return PROJECT_ROLES


# Adding Projects (ROLES)
def project_roles(update: Update, context: CallbackContext) -> int:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project roles.")
        return PROJECT_ROLES
    else:
        temp_project.append(update.message.text)

    update.message.reply_text("Please enter project deadline.")
    return PROJECT_DEADLINE


# Adding Projects (DEADLINE)
def project_deadline(update: Update, context: CallbackContext) -> int:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project deadline.")
        return PROJECT_DEADLINE
    else:
        temp_project.append(update.message.text)

    update.message.reply_text("Please enter project requirement.")
    return PROJECT_REQUIREMENTS


# Adding Projects (DEADLINE)
def project_requirement(update: Update, context: CallbackContext) -> int:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project requirement.")
        return PROJECT_REQUIREMENTS
    else:
        temp_project.append(update.message.text)

    update.message.reply_text("Please enter project team.")
    return PROJECT_TEAM


# Adding Projects (TEAM)
def project_team(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project team.")
        return PROJECT_TEAM
    else:
        temp_project.append(update.message.text)

    keyboard = [[InlineKeyboardButton("Yes", callback_data="Yes")],
                [InlineKeyboardButton("No", callback_data="No")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Please confirm project details.\n\n"
                         + view_projects(temp_project),
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN)

    return PROJECT_CONFIRM


# Adding Projects (CONFIRM
def project_confirm(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == "Yes":
        query.edit_message_text(f"Successfully added {temp_project[0]}.")
        context.bot_data["projects"].append(temp_project.copy())
        temp_project.clear()
        return ConversationHandler.END
    else:
        query.edit_message_text("Cancelled.")
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
