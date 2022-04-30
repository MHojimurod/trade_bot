from admin_panel.models import BotSettings, BusketItem, Category, Product
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
        user.send_message(**db.category_list(context=context,
                          user=db), parse_mode="HTML")
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
                'month': None if not x else x.month
            }
            update.callback_query.message.delete()
            user.send_photo(
                **db.product_info(context, True, db), parse_mode="HTML")
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
            **db.product_info(context,False, db), parse_mode="HTML")

    def back_to_category_from_product(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['current_product'] = None
        print(context.user_data['order'])
        update.callback_query.message.delete()
        user.send_message(
            **db.product_list(1,  context.user_data['order']['current_category']), parse_mode="HTML")

    def back_to_category_from_category(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        if context.user_data['order']['current_category']:
            context.user_data['order']['current_category'] = context.user_data['order']['current_category'].parent
            update.callback_query.message.edit_text(
                **db.category_list(1,  context.user_data['order']['current_category'], context, user=db))
        else:
            update.callback_query.message.delete()
            context.user_data['temp_message'] = user.send_message(
                db.text("mainMenu"), reply_markup=ReplyKeyboardMarkup(db.menu()), parse_mode="HTML")
            return MENU

    def add_to_cart(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        if context.user_data['order']['current_product']:
            if context.user_data['order']['current_product']['month'] is None:
                update.callback_query.answer("Iltimos kredit muddatini tallang!", True)
                return
            product = context.user_data['order']['current_product']

            db.busket.add(product['product'], product['count'], product['month'])
            context.user_data['order']['current_product'] = None
            update.callback_query.answer(db.text("product_added_to_busket"),True)
            update.callback_query.message.delete()
            user.send_message(
                **db.category_list(1,  None, context, user=db), parse_mode="HTML")

        else:
            raise

    def cart(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        if not context.user_data.get('order'):
            context.user_data['order'] = {}
        if update.message:
            update.message.delete()
            
            try:
                context.user_data['temp_message'].delete()
            except:
                pass
            if db.busket.is_available:
                user.send_message(
                    **db.cart(context, db, False), parse_mode="HTML")
            else:
                user.send_message(db.text("cart_empty"), reply_markup=ReplyKeyboardMarkup(
                    db.menu()), parse_mode="HTML")
                return MENU
        else:
            if db.busket.is_available:
                update.callback_query.message.edit_text(
                    **db.cart(context, db))
            else:
                user.send_message(db.text("cart_empty"), reply_markup=ReplyKeyboardMarkup(
                    db.menu()), parse_mode="HTML")
                return MENU
        return CART

    def remove_from_cart(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")
        BusketItem.objects.filter(id=data[1]).delete()
        if db.busket.is_available:

            update.callback_query.message.edit_text(
                **db.cart(context, db))
        else:
            update.callback_query.answer(db.text("nothing_in_busket"), True)
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
            db.text("mainMenu"), reply_markup=ReplyKeyboardMarkup(db.menu()), parse_mode="HTML")
        return MENU
    
    def back_to_menu(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        (update.message if update.message else update.callback_query.message).delete()
        context.user_data['temp_message'] = user.send_message(
            db.text("mainMenu"), reply_markup=ReplyKeyboardMarkup(db.menu()), parse_mode="HTML")
        return MENU


    def cart_product_count(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        data = update.callback_query.data.split(":")
        if data[1] == "+":
            BusketItem.objects.filter(id=data[2]).first().count += 1
        elif data[1] == "-":
            BusketItem.objects.filter(id=data[2]).first().count -= 1
        update.callback_query.message.edit_text(
            **db.cart(context, db))
    
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
            **db.product_info(context, False, db), parse_mode="HTML")

    def order_cart(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        update.callback_query.message.delete()
        context.user_data['temp_message'] = user.send_message(
            db.text('send_location'), reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(
                            db.text('send_location_button'), request_location=True)
                    ],
                    [
                        KeyboardButton(db.text("skip_location"))
                    ]
                ],
                resize_keyboard=True
            ), parse_mode="HTML")
        return CART_ORDER_LOCATION

    @remove_temp_message
    def cart_order_location(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        loc = update.message.location
        b =  db.busket.set_location(loc.latitude, loc.longitude)

        context.user_data['order']['location'] = update.message.location.to_dict()

        # context.user_data['temp_message'] = user.send_message(
        #     db.text('send_your_self_image'), parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        context.user_data['temp_message'] = user.send_photo(photo=BotSettings.objects.first().request_self_image, caption=db.text("send_your_self_image"), parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

        return CART_ORDER_SELF_IMAGE
    
    def skip_location(self, update:Update, context:CallbackContext):
        user, db = get_user(update)

        context.user_data['order']['location'] = None

        # context.user_data['temp_message'] = user.send_message(
            # db.text('send_your_self_image'), parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        context.user_data['temp_message'] = user.send_photo(photo=BotSettings.objects.first().request_self_image, caption=db.text("send_your_self_image"), parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        return CART_ORDER_SELF_IMAGE
    
    def error_location(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        update.message.delete()
        user.send_message(db.text('location_error'), reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(
                            db.text('send_location_button'), request_location=True)
                    ],
                    [
                        KeyboardButton(db.text("skip_location"))
                    ]
                ],
                resize_keyboard=True
            ))

    @remove_temp_message
    def cart_order_self_image(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['self_image'] = update.message.photo[-1].get_file().download()
        db.busket.set_self_image(
            update.message.photo[-1].get_file().download())
        # context.user_data['temp_message'] = user.send_message(
        #     db.text('send_your_password_iamge'), parse_mode="HTML")
        context.user_data['temp_message'] = user.send_photo(photo=BotSettings.objects.first().request_passport_image, caption=db.text("send_your_password_iamge"), parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        return CART_ORDER_PASSPORT_IMAGE

    @remove_temp_message
    def cart_order_passport_image(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['passport_image'] = update.message.photo[-1].file_id
        db.busket.set_passport_image(
            update.message.photo[-1].get_file().download())
        # context.user_data['temp_message'] = user.send_message(
        #     db.text('send_your_self_and_passport_image'), parse_mode="HTML")
        context.user_data['temp_message'] = user.send_photo(photo=BotSettings.objects.first().request_self_passport_image,
        caption=db.text("send_your_self_and_passport_image"), parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        return CART_ORDER_SELF_PASSWORD_IMAGE

    @remove_temp_message
    def cart_order_self_password_image(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['self_passport_image'] = update.message.photo[-1].file_id
        db.busket.set_self_passport_image(
            update.message.photo[-1].get_file().download())
        user.send_message(db.text('is_your_number',number=db.number), reply_markup=ReplyKeyboardMarkup(
            [
                [
                    "✅" + db.text('yes'),
                   "❌" + db.text('no')
                ]
            ],
            resize_keyboard=True
        ), parse_mode="HTML")

        return CART_ORDER_CHECK_NUMBER
    
    def cart_order_check_number(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        if update.message.text.startswith("✅"):
            user.send_message(
                db.text('your_order_accepted'), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
            db.busket.order()
            user.send_message(
                db.text("mainMenu"), reply_markup=ReplyKeyboardMarkup(db.menu()), parse_mode="HTML")
            return MENU
        else:
            user.send_message(
                db.text('send_number_as_text'), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
            return GET_NUMBER_FOR_ORDER
    
    def get_number_for_order(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        context.user_data['order']['number'] = update.message.text
        db.busket.set_extra_number(update.message.text)
        db.busket.order()
        user.send_message(db.text('your_order_accepted'),
                          reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        return self.back_to_menu(update, context)
    
    def error_self_image(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        update.message.delete()
        user.send_message(
            db.text('send_your_self_image_error'), parse_mode="HTML")
        return CART_ORDER_SELF_IMAGE
    
    def error_passport_image(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        update.message.delete()
        user.send_message(
            db.text('send_your_passport_image_error'), parse_mode="HTML")
        return CART_ORDER_PASSPORT_IMAGE
        
    def error_self_passport_image(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        update.message.delete()
        user.send_message(
            db.text('send_your_self_password_image_error'), parse_mode="HTML")
        return CART_ORDER_SELF_PASSWORD_IMAGE