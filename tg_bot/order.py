from math import prod
from tkinter import E

from admin_panel.models import Busket, BusketItem, Category, Product
from telegram import *
from telegram.ext import *

from tg_bot.constants import CART, MENU, ORDER
from tg_bot.utils import get_user, remove_temp_message


class Order:
    @remove_temp_message
    def order(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order'] = {

            'current_category': None
        }
        context.user_data['cart'] = []
        user.send_message(**db.category_list(context=context, user=db))
        return ORDER

    def category_list(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")

        update.callback_query.message.edit_text(
            **db.category_list(int(data[1]), None, context, db))

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
                    **db.category_list(1,  context.user_data['order']['current_category'], context, user=db))
        else:
            raise

    def select_product(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")

        product: Product = Product.objects.filter(id=int(data[1])).first()

        if product:
            x = db.busket.products.filter(product=product).first()
            context.user_data['order']['current_product'] = {
                'count': 1 if not x else x.count,
                'product': product,
                'month': product.color.months.filter(months=3).first()
            }

            update.callback_query.message.edit_text(
                **db.product_info(context))
        else:
            raise

    def product_count(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")
        if data[1] == "+":
            context.user_data['order']['current_product']['count'] += 1
        elif data[1] == "-":
            context.user_data['order']['current_product']['count'] -= 1
        else:
            if context.user_data['order']['current_product']['count'] == int(data[1]):
                return
            context.user_data['order']['current_product']['count'] = int(
                data[1])
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
                **db.category_list(1,  context.user_data['order']['current_category'], context, user=db))
        else:
            update.callback_query.message.delete()
            context.user_data['temp_message'] = user.send_message(
                "Salom", reply_markup=ReplyKeyboardMarkup(db.menu()))
            return MENU

    def add_to_cart(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        if context.user_data['order']['current_product']:
            product = context.user_data['order']['current_product']

            db.busket.add(product['product'], product['count'])
            context.user_data['order']['current_product'] = None
            update.callback_query.message.edit_text(
                **db.category_list(1,  None, context, user=db))
            update.callback_query.answer("Mahsulot savatga qo'shildi!")

        else:
            raise

    def cart(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        if update.message:
            update.message.delete()
            try:
                context.user_data['temp_message'].delete()
            except:
                pass
            user.send_message(
                **db.cart(context, db, False))
        else:
            update.callback_query.message.edit_text(
                **db.cart(context, db))
        return CART

    def remove_from_cart(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")
        BusketItem.objects.filter(id=data[1]).delete()
        if db.busket.is_available:

            update.callback_query.message.edit_text(
                **db.cart(context, db))
        else:
            update.callback_query.answer("savatda hech nimaqomadi!")
            update.callback_query.message.edit_text(
                **db.category_list(1,  None, context, user=db))
            return ORDER

    def back_to_category_from_cart(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        cat: Category = context.user_data['order']['current_category']
        if cat and cat.products().count() > 0:

            update.callback_query.message.edit_text(
                **db.product_list(1,  context.user_data['order']['current_category']))
        else:
            update.callback_query.message.edit_text(
                **db.category_list(1,None, context, db))
        return ORDER
    
    def back_to_menu_from_category(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        update.callback_query.message.delete(  )
        context.user_data['temp_message'] = user.send_message(
            "Salom", reply_markup=ReplyKeyboardMarkup(db.menu()))
        return MENU


    def cart_product_count(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")
        if data[1] == "+":
            BusketItem.objects.filter(id=data[1]).first().count += 1
        elif data[1] == "-":
            BusketItem.objects.filter(id=data[1]).first().count -= 1
        update.callback_query.message.edit_text(
            **db.cart(context))
    
    def product_creadit_month(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")
        print("x")

        product: Product = context.user_data['order']['current_product']['product']
        new = product.color.months.filter(
            id=int(data[1])).first()
        if new == context.user_data['order']['current_product']['month']:
            return
        
        context.user_data['order']['current_product']['month'] = new

        update.callback_query.message.edit_text(
            **db.product_info(context))
