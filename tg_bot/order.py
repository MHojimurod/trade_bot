from math import prod
from os import remove
from tkinter import E

from admin_panel.models import Busket, BusketItem, Category, Product
from telegram import *
from telegram.ext import *

from tg_bot.constants import CART, CART_ORDER_CHECK_NUMBER, CART_ORDER_LOCATION, CART_ORDER_PASSPORT_IMAGE, CART_ORDER_SELF_IMAGE, CART_ORDER_SELF_PASSWORD_IMAGE, GET_NUMBER_FOR_ORDER, MENU, ORDER
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
            update.callback_query.message.delete()
            user.send_photo(
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
        update.callback_query.message.edit_caption(
            **db.product_info(context,False))

    def back_to_category_from_product(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['current_product'] = None
        print(context.user_data['order'])
        update.callback_query.message.delete()
        user.send_message(
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

            db.busket.add(product['product'], product['count'], product['month'])
            context.user_data['order']['current_product'] = None
            update.callback_query.message.delete()
            user.send_message(
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

        update.callback_query.message.edit_caption(
            **db.product_info(context, False))

    def order_cart(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        update.callback_query.message.delete()
        context.user_data['temp_message'] = user.send_message(
            "Iltimos manzilingizni yuboring!", reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(
                            "Send location", request_location=True)
                    ]
                ],
                resize_keyboard=True
            ))
        return CART_ORDER_LOCATION

    @remove_temp_message
    def cart_order_location(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['location'] = update.message.location.to_dict()
        context.user_data['temp_message'] = user.send_message(
            "Iltimos o'zingizni rasmingizni yuboring!")
        return CART_ORDER_SELF_IMAGE

    @remove_temp_message
    def cart_order_self_image(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['self_image'] = update.message.photo[-1].file_id
        context.user_data['temp_message'] = user.send_message(
            "Iltimos passportingizni rasmini yuboring!")
        return CART_ORDER_PASSPORT_IMAGE

    @remove_temp_message
    def cart_order_passport_image(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['passport_image'] = update.message.photo[-1].file_id
        context.user_data['temp_message'] = user.send_message(
            "Iltimos passportingiz bilan birga tushgan rasmingizni yuboring!")
        return CART_ORDER_SELF_PASSWORD_IMAGE

    @remove_temp_message
    def cart_order_self_password_image(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['self_passport_image'] = update.message.photo[-1].file_id
        user.send_message("Shu sizning raqamingiz ekanligini tasdiqlaysizmi?\n\n%s" % (db.number), reply_markup=ReplyKeyboardMarkup(
            [
                [
                    "✅ Ha",
                    "❌ Yo'q"
                ]
            ],
            resize_keyboard=True
        ))

        return CART_ORDER_CHECK_NUMBER
    
    def cart_order_check_number(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        if update.message.text == "✅ Ha":
            user.send_message(
                "Sizning buyurtmangiz qabul qilindi!\n\nOperatorlarimiz siz bilan tez orada bog'lanishadi!", reply_markup=ReplyKeyboardRemove())
            user.send_message(
                "Menu", reply_markup=ReplyKeyboardMarkup(**db.menu()))
            return MENU
        else:
            user.send_message(
                "Iltimos raqamingizni text ko'rinishida yuboring!", reply_markup=ReplyKeyboardRemove())
            return GET_NUMBER_FOR_ORDER
    
    def get_number_for_order(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['number'] = update.message.text
        user.send_message("Sizning buyurtmangiz qabul qilindi!\n\nOperatorlarimiz siz bilan tez orada bog'lanishadi!", reply_markup=ReplyKeyboardRemove())
        user.send_message(**db.menu())
        return MENU