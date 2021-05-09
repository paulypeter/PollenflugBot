"""Miscellanious commands"""

import subprocess
import datetime

from telegram import Update, ForceReply
from telegram.ext import CallbackContext, ConversationHandler

from .db import r

def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Mehr Infos zum Bot:\nhttps://paulypeter.github.io/PollenflugBot/')

def cancel(update: Update, _: CallbackContext) -> None:
    """Cancel current action."""
    update.message.reply_text('Aktion abgebrochen.')
    return ConversationHandler.END

def download(_: CallbackContext) -> None:
    """download current forecast"""
    cmd = ["./get_pollen_images.sh", "1", "2"]
    if datetime.date.today().weekday() == 4:
        cmd.append("3")
    subprocess.call(cmd)

def reset_day(_: CallbackContext) -> None:
    """clear received fields and delete non-subscribers"""
    subscribers = r.scan(0)[1]
    for user_id in subscribers:
        r.hset(user_id, "received_today", 'false')
        r.hset(user_id, "received_tomorrow", 'false')
        r.hset(user_id, "received_sunday", 'false')
        if r.hget(user_id, "delete") == 'true':
            r.delete(user_id)

def reset_today(_: Update, context: CallbackContext) -> None:
    """manually reset day"""
    reset_day(context)
