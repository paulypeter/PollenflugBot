#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Adapted from PTB v13.5
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

redis structure:
    "user_id" => "subscribed": 'true' or 'false,
                "received_today": 'true' or 'false,
                "received_tomorrow": 'true' or 'false,
                "pollen_type": list of int
"""

import datetime
import pytz

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from components.admin_tools import admin_reset, stats
from components.subscription_tools import change_pollen_type_handler, subscribe_handler, unsubscribe
from components.send_images import today, tomorrow, send_daily_img, daily_img, sunday
from components.messaging import (
    send_single_message_handler,
    subscriber_message_handler,
    feedback_handler,
    selected_subscriber
)
from components.misc_commands import start, help_command, reset_day, download #, reset_today
from components.error_handler import error_handler


# Define a few command handlers. These usually take the two arguments update and
# context.


def main() -> None:
    """Start the bot."""
    # Create the Updater with token from txt file
    f = open("token.txt", "r")
    token = f.read().strip()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("hilfe", help_command))
    dispatcher.add_handler(CommandHandler("heute", today))
    dispatcher.add_handler(CommandHandler("morgen", tomorrow))
    dispatcher.add_handler(CommandHandler("abo_abbestellen", unsubscribe))
    #dispatcher.add_handler(CommandHandler("send_daily_img", send_daily_img))
    dispatcher.add_handler(CommandHandler("admin_reset", admin_reset))
    dispatcher.add_handler(CommandHandler("stats", stats))

    # define some conversation headers
    dispatcher.add_handler(subscribe_handler)
    dispatcher.add_handler(change_pollen_type_handler)
    dispatcher.add_handler(feedback_handler)
    dispatcher.add_handler(subscriber_message_handler)
    dispatcher.add_handler(send_single_message_handler)
    dispatcher.add_handler(CallbackQueryHandler(selected_subscriber))


    # queue the daily commands
    queue = updater.job_queue
    job_daily = queue.run_daily(daily_img, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(
        hour=7, minute=0, tzinfo=pytz.timezone('Europe/Berlin')))
    job_daily = queue.run_daily(reset_day, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(
        hour=6, minute=0, tzinfo=pytz.timezone('Europe/Berlin')))

    job_daily = queue.run_daily(download, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(
        hour=5, minute=45, tzinfo=pytz.timezone('Europe/Berlin')))
    job_daily = queue.run_daily(download, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(
        hour=11, minute=20, tzinfo=pytz.timezone('Europe/Berlin')))
    

    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
