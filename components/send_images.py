"""everything related to sending images"""

import datetime
from ast import literal_eval

from telegram import files
from telegram import Update, ChatAction
from telegram.ext import CallbackContext


from .db import r
from .constants import POLLEN, DAY, FORECAST_DAY

def get_document_list(img_num, selection_array):
    """get list object"""
    res = []
    img_time = datetime.date.today() + datetime.timedelta(days=(img_num - 1))
    for pollen_type in selection_array:
        res.append(files.inputmedia.InputMediaDocument(
            open('pollen_{0}_{1}.png'.format(img_num, pollen_type), "rb"),
            caption=f'{POLLEN[pollen_type]}'))
    return res

def today(update: Update, context: CallbackContext) -> None:
    """request today's forecast"""
    user_id = update.message.from_user.id
    handle_day_forecast(update, context, user_id, 1)

def tomorrow(update: Update, context: CallbackContext) -> None:
    """request tomorrow's forecast"""
    user_id = update.message.from_user.id
    handle_day_forecast(update, context, user_id, 2)

def sunday(update: Update, context: CallbackContext) -> None:
    """request sunday's forecast"""
    if datetime.date.today().weekday() != 4:
        update.message.reply_text("Die Vorhersage gibt es nur freitags.")
        return
    user_id = update.message.from_user.id
    handle_day_forecast(update, context, user_id, 3)

def send_daily_img(_: Update, context: CallbackContext) -> None:
    """manually send the daily image"""
    daily_img(context)

def daily_img(context: CallbackContext) -> None:
    """send daily update"""
    for user_id in r.keys(pattern="*"):
        pollen_type = literal_eval(r.hget(user_id, "pollen_type"))
        if pollen_type:
            send_one_or_multiple(context, user_id, 1, pollen_type)

def handle_day_forecast(update: Update, context: CallbackContext, user_id, img_num) -> None:
    """ handle forecast request for given day """
    if str(user_id) in r.keys(pattern="*"):
        if r.hget(user_id, f"received_{DAY[img_num - 1]}") in ['false', 'None']:
            pollen_type = literal_eval(r.hget(user_id, "pollen_type"))
            if pollen_type:
                send_one_or_multiple(context, user_id, img_num, pollen_type)
            else:
                update.message.reply_text("Es wurde keine Pollenart ausgewählt!")
        else:
            update.message.reply_text(f"Die {FORECAST_DAY[img_num - 1]}Vorhersage wurde bereits gesendet.")
    else:
        update.message.reply_text("Das funktioniert nur mit Abo.")

def send_one_or_multiple(context: CallbackContext, user_id, img_num, pollen_type) -> None:
    """ send forecast """
    r.hset(user_id, f"received_{DAY[img_num - 1]}", 'true')
    img_time = datetime.date.today() + datetime.timedelta(days=(img_num - 1))
    context.bot.send_message(chat_id=user_id,
        text=f'Vorhersage für den {img_time.strftime("%d.%m.%Y")}:')
    context.bot.send_chat_action(chat_id=user_id, action=ChatAction.UPLOAD_DOCUMENT)
    if len(pollen_type) == 1:
        path = 'pollen_{0}_{1}.png'.format(img_num, pollen_type[0])
        context.bot.send_document(chat_id=user_id,
                document=open(path, "rb"),
                caption=f'{POLLEN[pollen_type[0]]}')
    else:
        context.bot.send_media_group(chat_id=user_id,
            media=get_document_list(img_num, pollen_type))
