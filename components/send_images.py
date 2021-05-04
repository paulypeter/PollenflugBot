"""everything related to sending images"""

import datetime

from telegram import files
from telegram import Update, ChatAction
from telegram.ext import CallbackContext


from .db import r
from .constants import POLLEN

def get_img_num():
    """should be removed"""
    return 1

def get_document_list(img_num, selection_array):
    """get list object"""
    res = []
    img_time = datetime.date.today() + datetime.timedelta(days=(img_num - 1))
    for pollen_type in selection_array:
        res.append(files.inputmedia.InputMediaDocument(
            open('pollen_{0}_{1}.png'.format(img_num, pollen_type), "rb"),
            caption=f'{POLLEN[pollen_type]}, {img_time}'))
    return res

def today(update: Update, context: CallbackContext) -> None:
    """send today's forecast"""
    user_id = update.message.from_user.id
    if str(user_id) in r.keys(pattern="*"):
        if r.hget(user_id, "received_today") in ['false', 'None']:
            img_num = get_img_num()
            pollen_type = eval(r.hget(user_id, "pollen_type"))
            if pollen_type:
                r.hset(user_id, "received_today", 'true')
                if len(pollen_type) == 1:
                    path = 'pollen_{0}_{1}.png'.format(img_num, pollen_type[0])
                    context.bot.send_chat_action(chat_id=user_id, action=ChatAction.UPLOAD_DOCUMENT)
                    context.bot.send_document(chat_id=user_id,
                            document=open(path, "rb"),
                            caption=f'{POLLEN[pollen_type[0]]}, {datetime.date.today()}')
                else:
                    context.bot.send_chat_action(chat_id=user_id, action=ChatAction.UPLOAD_DOCUMENT)
                    context.bot.send_media_group(chat_id=user_id,
                        media=get_document_list(img_num, pollen_type))
            else:
                update.message.reply_text("Es wurde keine Pollenart ausgewählt!")
        else:
            update.message.reply_text("Die heutige Vorhersage wurde bereits gesendet.")
    else:
        update.message.reply_text("Das funktioniert nur mit Abo.")

def tomorrow(update: Update, context: CallbackContext) -> None:
    """send tomorrow's forecast"""
    user_id = update.message.from_user.id
    if str(user_id) in r.keys(pattern="*"):
        if r.hget(user_id, "received_tomorrow") in ['false', 'None']:
            img_num = get_img_num() + 1
            pollen_type = eval(r.hget(user_id, "pollen_type"))
            if pollen_type:
                r.hset(user_id, "received_tomorrow", 'true')
                if len(pollen_type) == 1:
                    path = 'pollen_{0}_{1}.png'.format(img_num, pollen_type[0])
                    context.bot.send_chat_action(chat_id=user_id, action=ChatAction.UPLOAD_DOCUMENT)
                    context.bot.send_document(chat_id=user_id,
                            document=open(path, "rb"),
                            caption=f'{POLLEN[pollen_type[0]]}, {datetime.date.today()}')
                else:
                    context.bot.send_chat_action(chat_id=user_id, action=ChatAction.UPLOAD_DOCUMENT)
                    context.bot.send_media_group(chat_id=user_id,
                        media=get_document_list(img_num, pollen_type))
            else:
                update.message.reply_text("Es wurde keine Pollenart ausgewählt!")
        else:
            update.message.reply_text("Die morgige Vorhersage wurde bereits gesendet.")
    else:
        update.message.reply_text("Das funktioniert nur mit Abo.")

def send_daily_img(_: Update, context: CallbackContext) -> None:
    """manually send the daily image"""
    daily_img(context)

def daily_img(context: CallbackContext) -> None:
    """send daily update"""
    img_num = get_img_num()
    for user_id in r.keys(pattern="*"):
        pollen_type = eval(r.hget(user_id, "pollen_type"))
        if pollen_type:
            if len(pollen_type) == 1:
                path = 'pollen_{0}_{1}.png'.format(img_num, pollen_type[0])
                context.bot.send_document(chat_id=user_id,
                        document=open(path, "rb"),
                        caption=f'{POLLEN[pollen_type[0]]}, {datetime.date.today()}')
            else:
                context.bot.send_media_group(chat_id=user_id,
                    media=get_document_list(img_num, pollen_type))
