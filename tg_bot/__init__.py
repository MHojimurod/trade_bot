from email.message import Message
import time

from flask import Flask, jsonify, request
from telegram import ReplyKeyboardMarkup, Update
from admin_panel.models import Ads, Busket, User
from tg_bot.filters import MultiLanguageFilter, MultilanguageMessageHandler

from tg_bot.myorders import myOrders
from tg_bot.utils import get_user
from .settings import Settings
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from .constants import (
    ADDRESS, AKSIYA, CART, CART_ORDER_CHECK_NUMBER, CART_ORDER_LOCATION, CART_ORDER_PASSPORT_IMAGE, CART_ORDER_SELF_IMAGE, CART_ORDER_SELF_PASSWORD_IMAGE, FILIAL, GET_NUMBER_FOR_ORDER, LIVE_PLACE, MY_ORDERS, ORDER, OUR_ADDRESSES, SETTINGS, SETTINGS_FILIAL, SETTINGS_LANGUAGE, SETTINGS_NAME, SETTINGS_NUMBER, SUPPORT, TOKEN, LANGUAGE, NAME, NUMBER,MENU, WORK_PLACE
)
from .basehandlers import Basehandlers
from .order import Order





class Bot(Updater, Basehandlers, Order, Settings, myOrders):
    def __init__(self,*args, **kwargs):

        super().__init__(TOKEN, *args, **kwargs)

        not_start = ~Filters.regex("^/start$")


        self.conversation = ConversationHandler(
            [
                CommandHandler('start', self.start),
            ],
            {
                LANGUAGE: [
                    MessageHandler(Filters.text & not_start, self.language),
                ],
                NAME: [
                    MessageHandler(Filters.text & not_start, self.name),
                ],
                NUMBER: [
                    MessageHandler(Filters.contact, self.number),
                    MessageHandler(Filters.regex(
                        "(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})") | Filters.regex(
                        "(?:[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"), self.number),
                    MessageHandler(Filters.text, self.number_error2)
                ],
                FILIAL: [
                    MessageHandler(Filters.text & not_start, self.filial)
                ],
                MENU: [
                    MultilanguageMessageHandler(
                        "order", self.order
                    ),
                    MultilanguageMessageHandler(
                        "my_orders", self.my_orders
                    ),
                    MultilanguageMessageHandler(
                        "busket", self.cart
                    ),

                    
                    MultilanguageMessageHandler(
                        "communications", self.contact_with_phone
                    ),
                    MultilanguageMessageHandler(
                        "settings", self.settings
                    ),

                    MultilanguageMessageHandler(
                        "our_addresses", self.our_addresses
                    ),

                    MultilanguageMessageHandler(
                        "questions_and_adds", self.support
                    ),
                    MultilanguageMessageHandler(
                        "offers", self.aksiya
                    ),
                ],
                ORDER: [
                    CallbackQueryHandler(
                        self.category_list, pattern="^category_pagination:"),
                    CallbackQueryHandler(
                        self.enter_category, pattern="^select_category:"),
                    CallbackQueryHandler(
                        self.select_product, pattern="^select_product:"),
                    CallbackQueryHandler(
                        self.product_count, pattern="^product_count:"),
                    CallbackQueryHandler(
                        self.back_to_category_from_product, pattern="^back_to_category_from_product"),
                    CallbackQueryHandler(
                        self.back_to_category_from_category, pattern="^back_to_category_from_category"),
                    CallbackQueryHandler(
                        self.product_creadit_month, pattern="^product_creadit_month"
                    ),
                    CallbackQueryHandler(
                        self.add_to_cart, pattern="add_to_cart"),
                    CallbackQueryHandler(
                        self.cart, pattern="^cart"),
                ],
                CART: [
                    # controls counts
                    CallbackQueryHandler(
                        self.cart_add_more, pattern="^cart_add_more"),
                    
                    CallbackQueryHandler(
                        self.cart_product_count, pattern="^cart_item_count:"),
                    CallbackQueryHandler(
                        self.remove_from_cart, pattern="^remove_from_cart:"),
                    CallbackQueryHandler(
                        self.back_to_category_from_cart, pattern="^back_to_category_from_cart"),
                    CallbackQueryHandler(
                        self.order_cart, pattern="^order_cart"),
                    CallbackQueryHandler(
                        self.back_to_category_from_category, pattern="^back_to_category_from_category"),
                ],
                CART_ORDER_LOCATION: [
                    MessageHandler(Filters.location, self.cart_order_location),
                    MultilanguageMessageHandler(
                        "skip_location", self.skip_location
                    ),
                    MessageHandler(Filters.text, self.error_location)
                ],
                CART_ORDER_SELF_IMAGE:[
                    MessageHandler(Filters.photo, self.cart_order_self_image),
                    MessageHandler(Filters.text & not_start, self.error_self_image)
                ],
                CART_ORDER_PASSPORT_IMAGE: [
                    MessageHandler(Filters.photo, self.cart_order_passport_image),
                    MessageHandler(Filters.text & not_start, self.error_passport_image)
                ],
                CART_ORDER_SELF_PASSWORD_IMAGE: [
                    MessageHandler(Filters.photo, self.cart_order_self_password_image),
                    MessageHandler(Filters.text & not_start, self.error_self_passport_image)
                ],
                WORK_PLACE: [
                    MessageHandler(Filters.text & not_start, self.work_place)
                ],
                LIVE_PLACE: [
                    MessageHandler(Filters.text & not_start, self.live_place)
                ],
                CART_ORDER_CHECK_NUMBER: [
                    MessageHandler(
                        Filters.regex("^(???|???)"), self.cart_order_check_number
                    ),
                    MessageHandler(Filters.text & not_start, self.error_check_number)
                ],
                GET_NUMBER_FOR_ORDER: [
                    MessageHandler(Filters.regex(
                        "(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})") | Filters.regex(
                        "(?:[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"), self.get_number_for_order),
                    MessageHandler(Filters.text, self.error_text_number)
                ],
                SETTINGS: [
                    # MessageHandler(Filters.regex("^(Ismni o'zgartirish)$"), self.settings_name),
                    MultilanguageMessageHandler(
                        "change_name", self.settings_name
                    ),
                    # MessageHandler(Filters.regex("^(Tilni o'zgartirish)$"), self.settings_language),
                    MultilanguageMessageHandler(
                        "change_language", self.settings_language
                    ),
                    # MessageHandler(Filters.regex("^(Raqamni o'zgartirish)$"), self.settings_number),
                    MultilanguageMessageHandler(
                        "change_number", self.settings_number
                    ),
                    # MessageHandler(Filters.regex("^(Filialni o'zgartirish)$"), self.settings_change_filial),
                    MultilanguageMessageHandler(
                        "change_filial", self.settings_change_filial
                    ),
                    MultilanguageMessageHandler(
                        "back", self.back_to_menu
                    ),
                ],
                SETTINGS_NAME: [
                    
                    MessageHandler(Filters.text & not_start & ~MultiLanguageFilter("back"), self.settings_name_change),
                    MessageHandler(MultiLanguageFilter("back"), self.settings)
                ],
                SETTINGS_NUMBER: [
                    MessageHandler(Filters.contact, self.settings_number_change),
                    MessageHandler(Filters.regex(
                        "(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})") | Filters.regex(
                        "(?:[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"), self.settings_number_text),
                         MessageHandler(MultiLanguageFilter("back"), self.settings),
                    MessageHandler(Filters.text & not_start, self.settings_number_error),
                    
                ],
                SETTINGS_LANGUAGE: [
                    MessageHandler(Filters.text & not_start & ~MultiLanguageFilter("back"), self.settings_language_change),
                    MessageHandler(MultiLanguageFilter("back"), self.settings)
                ],
                SETTINGS_FILIAL: [
                    MessageHandler(Filters.text & not_start & ~MultiLanguageFilter("back"), self.settings_change_filial_change ),
                    MultilanguageMessageHandler('back', self.settings)
                ],
                OUR_ADDRESSES: [
                    MultilanguageMessageHandler('back', self.back_to_menu),
                    MessageHandler(Filters.text & not_start, self.address)
                ],
                SUPPORT: [
                    MessageHandler(Filters.text, self.support_message),
                    MessageHandler(
                        Filters.photo,
                        self.support_photo
                    ),
                    MessageHandler(
                        Filters.video,
                        self.support_video
                    ),
                ],
                AKSIYA: [CallbackQueryHandler(
                        self.aksiya, pattern="^back_to_aksiyas"),
                    MultilanguageMessageHandler('back', self.back_to_menu),
                    MessageHandler(Filters.text & not_start, self.aksiya_select),
                    
                ],
                MY_ORDERS: [
                    CallbackQueryHandler(self.my_orders, pattern="my_orders")
                ]

            },
            [
                CommandHandler('start', self.start),
                MessageHandler(Filters.all, self.start),
                CallbackQueryHandler(self.back_to_menu, pattern="^back_to_menu"),
            ]
        )

        self.dispatcher.add_handler(CommandHandler('dfsfsdfsfsdf', self.komiljonovaabddfsfgdgdfgdfgdfgdfg))
        

        self.dispatcher.add_handler(self.conversation)


        self.start_polling()
        server = Flask(__name__)

        server.route('/send_ads')(self.send_ads)
        server.route('/order_updated')(self.order_updated)
        server.route('/send_sms')(self.send_sms)

        server.run(port=6002)
        
        self.idle()
    def komiljonovaabddfsfgdgdfgdfgdfgdfg(self, update: Update, context: CallbackContext):
        update.message.reply_text("Komiljonovaabddfsfgdgdfgdfgdfgdfg")
        update.message.reply_text('stopped')
        self.stop()



    def error_check_number(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        user.send_message(db.text("error_check_number"), reply_markup=ReplyKeyboardMarkup(
            [
                [
                    "???" + db.text('yes'),
                   "???" + db.text('no')
                ]
            ],
            resize_keyboard=True
        ))
    

    def error_text_number(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        user.send_message(db.text("error_text_number"))

    def number_error2(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        user.send_message("Iltimos raqamingizni yuboring yoki pastdagi tugmani bosing!")
        return NUMBER

    
    def order_updated(self):
        data = request.get_json()
        status, order = data['status'], data['order']
        order:Busket = Busket.objects.filter(id=int(order)).first()
        if order:
            if status == 1:
                self.bot.send_message(order.user.chat_id, order.user.text("order_checking")  )
            elif status == 2:
                self.bot.send_message(order.user.chat_id, order.user.text("order_rejected",cause=order.comment)  )
            elif status == 3:
                self.bot.send_message(order.user.chat_id, order.user.text("order_accepted") )
            elif status == 4:
                self.bot.send_message(order.user.chat_id, order.user.text("order_not_accepted",cause=order.comment)  )
        return "ok"

    def send_ads(self):
        data = request.get_json()['data']
        ad = data['id']
        ad: Ads = Ads.objects.filter(id=ad).first()
        per = 0
        if ad:
            for user in User.objects.all():
                try:
                    print("sending")
                    if ad.mode == 0:
                        self.bot.send_message(user.chat_id, text=ad.send_desc(), parse_mode="HTML")
                    elif ad.mode == 1:
                        self.bot.send_photo(user.chat_id, photo=open(f".{ad.photo.url}", "rb"), caption=ad.send_desc(), parse_mode="HTML")
                    elif ad.mode == 2:
                        self.bot.send_video(user.chat_id, video=open(f".{ad.photo.url}", "rb"), caption=ad.send_desc(), parse_mode="HTML")
                except Exception as e:
                    print('user not found', e)
                per += 1
                if per == 20:
                    time.sleep(1)
                    per = 0
            return "ok"
        else:
            return jsonify({'status': 'error'})

    # @remove_temp_message
    def cart_add_more(self, update:Update, context:CallbackContext):
        (update.message if update.message else update.callback_query.message).delete()
        return self.order(update, context)
    
    def send_sms(self):
        data = request.get_json()['data']
        print(data)
        user: User = User.objects.filter(id=data["id"]).first()
        if user:
            try:
                self.bot.send_message(user.chat_id, data["message"])
            except:
                pass