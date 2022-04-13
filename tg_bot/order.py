from math import prod
from telegram import *
from telegram.ext import *
from tg_bot.constants import MENU, ORDER

from tg_bot.utils import get_user, remove_temp_message

from admin_panel.models import Category, Product


class Order:
    @remove_temp_message
    def order(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        context.user_data['order'] = {

            'current_category': None
        }
        context.user_data['cart'] = []
        user.send_message(**db.category_list(context=context))
        return ORDER
    
    def category_list(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")
        

        update.callback_query.message.edit_text(**db.category_list(int(data[1]),None, context))
    
    def enter_category(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")

        category: Category = Category.objects.filter(id=int(data[1])).first()
        context.user_data['order']['current_category'] = category
        if category:
            
            products = category.products()
            if products:
                
                update.callback_query.message.edit_text(
                    **db.product_list(1,  context.user_data['order']['current_category']))
            else:
                update.callback_query.message.edit_text(
                    **db.category_list(1,  context.user_data['order']['current_category'],context))
        else:
            raise
    
    def select_product(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")

        product: Product = Product.objects.filter(id=int(data[1])).first()

        if product:
            
            context.user_data['order']['current_product'] = {
                'count': 1,
                'product': product
            }
            update.callback_query.message.edit_text(
                **db.product_info(context))
        else:
            raise

    def product_count(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")
        if data[1] == "+":
            context.user_data['order']['current_product']['count'] += 1
        elif data[1] == "-":
            context.user_data['order']['current_product']['count'] -= 1
        else:
            if context.user_data['order']['current_product']['count'] == int(data[1]):
                return 
            context.user_data['order']['current_product']['count'] = int(data[1])
        update.callback_query.message.edit_text(
            **db.product_info(context))
    
    def back_to_category_from_product(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['current_product'] = None
        print(context.user_data['order'])
        update.callback_query.message.edit_text(
            **db.product_list(1,  context.user_data['order']['current_category']))
    
    def back_to_category_from_category(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        if context.user_data['order']['current_category']:
            context.user_data['order']['current_category'] = context.user_data['order']['current_category'].parent
            update.callback_query.message.edit_text(
            **db.category_list(1,  context.user_data['order']['current_category'], context))
        else:
            update.callback_query.message.delete()
            context.user_data['temp_message'] = user.send_message(
                "Salom", reply_markup=ReplyKeyboardMarkup(db.menu()))
            return MENU

    def add_to_cart(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        if context.user_data['order']['current_product']:
            product = context.user_data['order']['current_product']
            context.user_data['cart'].append({
                "product": product['product'],
                "count": product['count']
            })
            context.user_data['order']['current_product'] = None
            update.callback_query.message.edit_text(
                **db.category_list(1,  None, context))

        else:
            raise
    
    def cart(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        if context.user_data['cart']:
            update.callback_query.message.edit_text(
                **db.cart(context))
        else:
            pass