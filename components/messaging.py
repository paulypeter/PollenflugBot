"""Everything related to sending messages."""

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    Filters,
    MessageHandler
)

from .constants import INPUT_FEEDBACK, TYPE_MESSAGE, INPUT_MESSAGE, ADMIN
from .db import r
from .misc_commands import cancel

def send_feedback(update: Update, _: CallbackContext) -> None:
    """Initiate sending a feedback message"""
    update.message.reply_text("Bitte eine Nachricht eingeben:")
    return INPUT_FEEDBACK

def feedback_input(update: Update, context: CallbackContext) -> int:
    """Type feedback message"""
    username = update.message.from_user.username
    message = f'@{username} schreibt:\n' + update.message.text
    context.bot.send_message(chat_id=ADMIN, text=message)
    update.message.reply_text('Die Nachricht wurde gesendet!')
    return ConversationHandler.END

def send_single_message(update: Update, _: CallbackContext):
    """Admin method: send message to a single user"""
    if str(update.message.from_user.id) != ADMIN:
        return ConversationHandler.END
    keys = r.keys(pattern="*")
    keyboard = []
    for key in keys:
        keyboard.append([InlineKeyboardButton(key, callback_data=key)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text='Abonnent auswählen: ', reply_markup=reply_markup)
    return TYPE_MESSAGE

def selected_subscriber(update: Update, _: CallbackContext) -> int:
    """Callbackquery method when a subscriber was selected"""
    query = update.callback_query
    query.answer()
    if r.exists(query.data):
        r.hset(ADMIN, "send_message_to", query.data)
        query.message.reply_text('Bitte Nachricht eingeben:')
        return TYPE_MESSAGE
    return ConversationHandler.END

def type_message(update: Update, context: CallbackContext) -> int:
    """type a message to selected subscriber"""
    user_id = r.hget(ADMIN, "send_message_to")
    r.hdel(ADMIN, "send_message_to")
    message = update.message.text
    context.bot.send_message(chat_id=user_id, text=message)
    return ConversationHandler.END

def send_subscriber_message(update: Update, _: CallbackContext) -> None:
    """initiate sending a message to one subscriber"""
    if str(update.message.from_user.id) == ADMIN:
        message_text = 'Bitte Text eingeben:'
    else:
        message_text = "Sorry, nur für Admins!"
    update.message.reply_text(message_text)
    return INPUT_MESSAGE

def message_input(update: Update, context: CallbackContext) -> int:
    """type a message to all subscibers"""
    message = "Bleep Bloop\n" + update.message.text
    subscribers = r.keys(pattern="*")
    for sub in subscribers:
        context.bot.send_message(chat_id=sub, text=message)
    update.message.reply_text('Die Nachricht wurde gesendet!')
    return ConversationHandler.END

send_single_message_handler = ConversationHandler(
        entry_points = [CommandHandler("send_single_message", send_single_message)],
        states = {
            TYPE_MESSAGE: [MessageHandler(Filters.text & ~Filters.command, type_message)],
        },
        fallbacks=[CommandHandler('abbrechen', cancel)],
    )

subscriber_message_handler = ConversationHandler(
        entry_points = [CommandHandler("send_subscriber_message", send_subscriber_message)],
        states = {
           INPUT_MESSAGE : [MessageHandler(Filters.text & ~Filters.command, message_input)],
        },
        fallbacks=[CommandHandler('abbrechen', cancel)],
    )

feedback_handler = ConversationHandler(
        entry_points = [CommandHandler("feedback_senden", send_feedback)],
        states = {
           INPUT_FEEDBACK : [MessageHandler(Filters.text & ~Filters.command, feedback_input)],
        },
        fallbacks=[CommandHandler('abbrechen', cancel)],
    )
