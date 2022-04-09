from math import prod
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
    
    def enter_category(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")

        category: Category = Category.objects.filter(id=int(data[1])).first()

        if category:
            context.user_data['current_category'] = category
            products = category.products()
            if products:
                update.callback_query.message.edit_text(
                    **db.product_list(1,  context.user_data['current_category']))
            else:
                update.callback_query.message.edit_text(
                    **db.category_list(1,  context.user_data['current_category']))
        else:
            raise



