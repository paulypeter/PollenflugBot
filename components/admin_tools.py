"""Tools for the admin"""

from telegram import Update
from telegram.ext import CallbackContext

from .db import r
from .constants import ADMIN

def admin_reset(update: Update, _: CallbackContext) -> None:
    """for testing purposes"""
    if str(update.message.from_user.id) == ADMIN:
        r.hset(ADMIN, "received_today", 'false')
        r.hset(ADMIN, "received_tomorrow", 'false')
        r.hset(ADMIN, "received_sunday", 'false')
        message_text = "Fields reset"
    else:
        message_text = "Sorry, nur für Admins!"
    update.message.reply_text(message_text)

def stats(update: Update, _: CallbackContext) -> None:
    """get number of subscribers"""
    if str(update.message.from_user.id) == ADMIN:
        subscribers = r.keys(pattern="*")
        message_text = f'Es sind {len(subscribers)} Abonnenten eingetragen.'
    else:
        message_text = "Sorry, nur für Admins!"
    update.message.reply_text(message_text)
