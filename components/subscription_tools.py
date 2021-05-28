"""Methods handling subscriptions"""
from ast import literal_eval

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler

from .db import r
from .constants import SET_TYPE, POLLEN
from .misc_commands import cancel

def subscribe(update: Update, _: CallbackContext) -> None:
    """initiate subscription conversation"""
    user_id = update.message.from_user.id
    existing_user = True
    if not r.exists(user_id):
        r.hset(user_id, "subscribed", 'true')
        r.hset(user_id, "received_today", 'None')
        r.hset(user_id, "received_tomorrow", 'None')
        r.hset(user_id, "received_sunday", 'None')
        r.hset(user_id, "delete", 'false')
        r.hset(user_id, "pollen_type", str([2]))
        message_text = "PollenflugBot wurde erfolgreich abonniert."
        existing_user = False
        state = SET_TYPE
    elif not r.hget(user_id, "subscribed") or r.hget(user_id, "subscribed") == 'false':
        r.hset(user_id, "subscribed", 'true')
        r.hset(user_id, "delete", 'false')
        message_text = "PollenflugBot wurde erfolgreich abonniert."
        state = SET_TYPE
    else:
        message_text = "PollenflugBot ist bereits abonniert."
        state = ConversationHandler.END
    update.message.reply_text(message_text)
    if state == SET_TYPE:
        if existing_user:
            pollen_type = literal_eval(r.hget(user_id, "pollen_type"))
        else:
            pollen_type = []
        keyboard = pollen_keyboard(pollen_type)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text='Pollenart(en) auswählen: ', reply_markup=reply_markup)
        return SET_TYPE
    return ConversationHandler.END

def change_pollen_type(update: Update, _: CallbackContext) -> int:
    """get selection and start pollen selection"""
    user_id = update.message.from_user.id
    if r.exists(user_id):
        selection = literal_eval(r.hget(user_id, "pollen_type"))
    else:
        selection = []
    keyboard = pollen_keyboard(selection)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text='Pollenart(en) auswählen: ', reply_markup=reply_markup)
    return SET_TYPE

def select_pollen_type(update: Update, _: CallbackContext) -> int:
    """select pollen types"""
    query = update.callback_query
    query.answer()
    if query.data == '-1':
        query.edit_message_text(text='Pollenart(en) ausgewählt.')
        return ConversationHandler.END
    user_id = query.from_user.id
    if r.exists(user_id):
        selection = literal_eval(r.hget(user_id, "pollen_type"))
    else:
        selection = []
    pollen_type = int(query.data)
    toggle_select(pollen_type, selection)
    r.hset(user_id, "pollen_type", str(selection))
    r.hset(user_id, "delete", 'false')
    r.hset(user_id, "received_today", 'None')
    r.hset(user_id, "received_tomorrow", 'None')
    keyboard = pollen_keyboard(selection)
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text='Pollenart(en) auswählen: ', reply_markup=reply_markup)
    return SET_TYPE

def unsubscribe(update: Update, _: CallbackContext) -> None:
    """unsubscribe"""
    user_id = update.message.from_user.id
    r.hset(user_id, "subscribed", 'false')
    r.hset(user_id, "delete", 'true')
    update.message.reply_text('Abo abbestellt.')

def pollen_kb_button(pollen_index, selection_array):
    """create a button for the pollen keyboard"""
    button_text = POLLEN[pollen_index]
    if pollen_index in selection_array:
        button_text += " ✓"
    return InlineKeyboardButton(button_text, callback_data=pollen_index)

def toggle_select(pollen_index, selection_array):
    """select or deselect a pollen type"""
    if pollen_index in selection_array:
        list_index = selection_array.index(pollen_index)
        selection_array.pop(list_index)
    else:
        selection_array.append(pollen_index)

def pollen_keyboard(sel):
    """create the pollen keyboard"""
    return [
        [
            pollen_kb_button(0, sel),
            pollen_kb_button(1, sel)
        ],
        [
            pollen_kb_button(2, sel),
            pollen_kb_button(3, sel)
        ],
        [
            pollen_kb_button(4, sel),
            pollen_kb_button(5, sel)
        ],
        [
            pollen_kb_button(6, sel),
            pollen_kb_button(7, sel)
        ],
        [
            InlineKeyboardButton("Fertig", callback_data='-1'),
        ],
    ]

subscribe_handler = ConversationHandler(
    entry_points = [CommandHandler("abonnieren", subscribe)],
    states = {
        SET_TYPE: [CallbackQueryHandler(select_pollen_type)],
    },
    fallbacks=[CommandHandler('abbrechen', cancel)],
)

change_pollen_type_handler = ConversationHandler(
    entry_points = [CommandHandler("pollenart_wechseln", change_pollen_type)],
    states = {
        SET_TYPE: [CallbackQueryHandler(select_pollen_type)],
    },
    fallbacks=[CommandHandler('abbrechen', cancel)],
)
