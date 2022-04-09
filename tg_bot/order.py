from telegram import *
from telegram.ext import *
from tg_bot.constants import ORDER

from tg_bot.utils import get_user

from admin_panel.models import Category, Product


class Order:
    def order(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        user.send_message(**db.category_list())
        return ORDER
    
    def category_list(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")
        update.callback_query.message.edit_text(**db.category_list(int(data[1])))