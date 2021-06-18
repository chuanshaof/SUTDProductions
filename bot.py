from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, ConversationHandler, \
    CallbackQueryHandler, Dispatcher, PicklePersistence

import logging

import os

"""
git add .
git commit -m "changing python3 to python in Procfile"
git push heroku master
"""

WAIT_CODE, PROJECT_NAME, PROJECT_DESCRIPTION, PROJECT_POC, PROJECT_VENUE, PROJECT_PARTNERS, PROJECT_INSPIRATION, \
PROJECT_ROLES, PROJECT_DEADLINE, PROJECT_REQUIREMENTS, PROJECT_TEAM, PROJECT_CONFIRM, LIST_PROJECTS, SOCIALS, \
SUBSCRIBE, UNSUBSCRIBE, ANNOUNCE, START, REMOVE, EDIT, EDIT_CONFIRM, ANNOUNCE_QUERY = range(22)
temp_project = list()

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1544769823:AAFJK_Md3EV8AMWHJG4i9Qaxe_LhCP6Jb5E'
my_persistence = PicklePersistence(filename='my_file')

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)


# User Interface
# ---------------------------------------------------------------------------------------------#
def start(update: Update, context: CallbackContext) -> None:
    if "subscribe" not in context.bot_data:
        context.bot_data["subscribe"] = list()

    if any(update.message.from_user.id in sl for sl in context.bot_data["subscribe"]):
        keyboard = [[InlineKeyboardButton("Unsubscribe from our bot", callback_data=str(UNSUBSCRIBE))],
                    [InlineKeyboardButton("View projects", callback_data=str(LIST_PROJECTS))],
                    [InlineKeyboardButton("Suggest Project", url='https://forms.gle/gQppNaaFqKkCHhHw6')],
                    [InlineKeyboardButton("Join our telegram", url='https://t.me/joinchat/SME7jUkjNIcSKc9v')],
                    [InlineKeyboardButton("Socials", callback_data=str(SOCIALS))]]
    else:
        keyboard = [[InlineKeyboardButton("Subscribe to our bot", callback_data=str(SUBSCRIBE))],
                    [InlineKeyboardButton("View projects", callback_data=str(LIST_PROJECTS))],
                    [InlineKeyboardButton("Suggest Project", url='https://forms.gle/gQppNaaFqKkCHhHw6')],
                    [InlineKeyboardButton("Join our telegram", url='https://t.me/joinchat/SME7jUkjNIcSKc9v')],
                    [InlineKeyboardButton("Socials", callback_data=str(SOCIALS))]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text=f"Hello *{update.message.from_user.username}* and welcome to *SUTD Productions'* "
                         f"Video Project Telegram Bot! 👋\n\n"

                         f"This bot is a one-stop platform for you to share your wildest video ideas, "
                         f"or to join a team with others. Once enough people have opted into your idea, "
                         f"we will contact you via Telegram to begin. Ideate - find a team - get filming! 🎬\n\n"

                         f"We're excited to have you here! We'll be updating the Bot with project ideas "
                         f"as soon as they're received, so sit tight and get ready to make some videos! 🎥\n\n"

                         f"*Before you go, remember to:*\n"
                         f"📺 Subscribe to our [YouTube](https://www.youtube.com/user/SUTDProductions) channel\n"
                         f"📱 Invite your friends to our [Telegram](https://t.me/joinchat/SME7jUkjNIcSKc9v) community\n"
                         f"📷 Follow us on [Instagram](https://www.instagram.com/sutdproductions/)\n\n"

                         "Feel free to contact us directly at productions@club.sutd.edu.sg for any "
                         "questions or feedback!",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup)

    return START


# Start QueryHandler
def start_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    projects = format_project_list(update, context)

    for each in context.bot_data["projects"]:
        if query.data == "desc" + each[0]:
            keyboard = [[InlineKeyboardButton("Join Project", callback_data="join" + each[0])],
                        [InlineKeyboardButton("Go back", callback_data=str(LIST_PROJECTS))]]

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

    # View projects
    if query.data == str(LIST_PROJECTS):
        if len(context.bot_data["projects"]) == 0:
            query.edit_message_text("Sorry, there are no projects at the moment!")
            return ConversationHandler.END
        else:
            keyboard = list()
            for each in projects:
                project = InlineKeyboardButton(each, callback_data="desc" + each)
                keyboard.append([project])

            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text('To view more details of each project, click on the title.',
                                    reply_markup=reply_markup)

    # Social media list
    elif query.data == str(SOCIALS):
        keyboard = [[InlineKeyboardButton("Instagram", url='https://www.instagram.com/sutdproductions/')],
                    [InlineKeyboardButton("Website", url='https://sutd.productions')],
                    [InlineKeyboardButton("Youtube", url='https://www.youtube.com/user/SUTDProductions')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"Connect with us via the various social medias!", reply_markup=reply_markup)
        return ConversationHandler.END

    # Subscribe query
    elif query.data == str(SUBSCRIBE):
        context.bot_data["subscribe"].append([query.from_user.id, query.from_user.username])
        query.edit_message_text("Subscribed to SUTDProductions.")
        return ConversationHandler.END

    # Unsubscribe query
    elif query.data == str(UNSUBSCRIBE):
        for each in context.bot_data["subscribe"]:
            if each[0] == query.from_user.id:
                context.bot_data["subscribe"].remove(each)
                query.edit_message_text("Unsubscribed from SUTDProductions, we hope to see you again!")
                return ConversationHandler.END


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
        update.message.reply_text("Please enter project name.")
        return PROJECT_NAME


# Adding Projects (TITLE)
def project_name(update: Update, context: CallbackContext) -> int:
    if not update.message.text:
        update.message.reply_text("Please enter a valid project name.")
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

    bot.sendMessage(chat_id=update.message.chat_id,
                    text=view_projects(temp_project),
                    parse_mode=ParseMode.MARKDOWN)

    keyboard = [[InlineKeyboardButton("Yes", callback_data="Yes")],
                [InlineKeyboardButton("No", callback_data="No")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please confirm project details.", reply_markup=reply_markup)
    bot.sendMessage("YES")
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


# Removing projects
# ---------------------------------------------------------------------------------------------#
def remove(update: Update, context: CallbackContext) -> None:
    if "admin" not in context.bot_data:
        context.bot_data["admin"] = list()

    if update.message.from_user.id not in context.bot_data["admin"]:
        return
    else:
        if "projects" not in context.bot_data or len(context.bot_data["projects"]) == 0:
            context.bot_data["projects"] = list()
            update.message.reply_text("Sorry, there are no projects at the moment!")
            return
        else:
            projects = format_project_list(update, context)
            keyboard = list()

            for each in projects:
                project = InlineKeyboardButton(each, callback_data=each)
                keyboard.append([project])

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Please select the project name you want to remove.", reply_markup=reply_markup)
            return REMOVE


# Remove project (CONFIRM)
def remove_confirm(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    keyboard = [[InlineKeyboardButton("Yes", callback_data="Y")],
                [InlineKeyboardButton("No", callback_data="N")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    for each in context.bot_data["projects"]:
        # Each[0] represents the name
        if query.data == each[0]:
            query.edit_message_text(f"{view_projects(each)}\n"
                                    f"Please confirm project removal.",
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.MARKDOWN)
        if query.data == "Y":
            query.edit_message_text(f"{each[0]} has been successfully removed.")
            context.bot_data["projects"].remove(each)
            return ConversationHandler.END
        elif query.data == "N":
            query.edit_message_text("Cancelled.")
            return ConversationHandler.END


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


# Admin Verification
# ---------------------------------------------------------------------------------------------#
def admin(update: Update, context: CallbackContext) -> int:
    if "admin" not in context.bot_data:
        context.bot_data["admin"] = list()

    if update.message.from_user.id in context.bot_data["admin"]:
        update.message.reply_text("Already verified, you can now use /add, /remove, /edit, and /announce.")
        return ConversationHandler.END
    else:
        update.message.reply_text("Enter the admin code")
    return WAIT_CODE


# Admin Verification, step 2
def verify(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    code = ***REMOVED***

    if user_input == code:
        update.message.reply_text("Verified, you can now use /add, /remove, /edit, and /announce.")
        context.bot_data["admin"].append(update.message.from_user.id)
    else:
        update.message.reply_text("Invalid")
    return ConversationHandler.END


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


# Cancel action
def cancel(update: Update, context: CallbackContext) -> None:
    return ConversationHandler.END


# Check subscribed members
def check_subs(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(context.bot_data["subscribe"])
    return


# Announcement
# ---------------------------------------------------------------------------------------------#
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
    bot.sendMessage(chat_id="229599548",
                    text=announce_message,
                    parse_mode=ParseMode.MARKDOWN)
    query = update.callback_query

    if query.data == "Y":
        for each in context.bot_data["subscribe"]:
            forward_to = each[0]
            bot.sendMessage(chat_id="229599548",
                            text=str(forward_to))
            bot.sendMessage(chat_id=str(forward_to),
                            message_id=announce_message,
                            parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text("Successfully announced to subscribers.")
        return ConversationHandler.END

    elif query.data == "N":
        query.edit_message_text("Cancelled.")
        return ConversationHandler.END


# Random stuff
# ---------------------------------------------------------------------------------------------#
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


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, persistence=my_persistence, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("clear_admins", clear_admins))
    dp.add_handler(CommandHandler("check_subs", check_subs))

    # Start handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("start", start)
        ],
        states={
            START: [CallbackQueryHandler(start_query)]
        },
        fallbacks=[],
        allow_reentry=True
    ))

    # Remove handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("remove", remove)
        ],
        states={
            REMOVE: [CallbackQueryHandler(remove_confirm)]
        },
        fallbacks=[]
    ))

    # Edit handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("edit", edit)
        ],
        states={
            EDIT: [CallbackQueryHandler(edit_query)],
            EDIT_CONFIRM: [CallbackQueryHandler(edit_confirmation)]
        },
        fallbacks=[],
        allow_reentry=True
    ))

    # Admin handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("admin", admin)
        ],
        states={
            WAIT_CODE: [MessageHandler(Filters.text, verify)]
        },
        fallbacks=[]
    ))

    # Adding project
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("add", add)
        ],
        states={
            PROJECT_NAME: [MessageHandler(Filters.text & (~ Filters.command), project_name)],
            PROJECT_DESCRIPTION: [MessageHandler(Filters.text & (~ Filters.command), project_description)],
            PROJECT_POC: [MessageHandler(Filters.text & (~ Filters.command), project_poc)],
            PROJECT_VENUE: [MessageHandler(Filters.text & (~ Filters.command), project_venue)],
            PROJECT_PARTNERS: [MessageHandler(Filters.text & (~ Filters.command), project_partners)],
            PROJECT_INSPIRATION: [MessageHandler(Filters.text & (~ Filters.command), project_inspiration)],
            PROJECT_ROLES: [MessageHandler(Filters.text & (~ Filters.command), project_roles)],
            PROJECT_DEADLINE: [MessageHandler(Filters.text & (~ Filters.command), project_deadline)],
            PROJECT_REQUIREMENTS: [MessageHandler(Filters.text & (~ Filters.command), project_requirement)],
            PROJECT_TEAM: [MessageHandler(Filters.text & (~ Filters.command), project_team)],
            PROJECT_CONFIRM: [CallbackQueryHandler(project_confirm)]
        },
        fallbacks=[MessageHandler(Filters.command, cancel)],
        allow_reentry=True
    ))

    # Announce handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("announce", announce)
        ],
        states={
            ANNOUNCE_QUERY: [MessageHandler(Filters.all & (~ Filters.command), announcement_confirm)],
            ANNOUNCE: [CallbackQueryHandler(announcement)]
        },
        fallbacks=[],
        allow_reentry=True
    ))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://boiling-badlands-67618.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
