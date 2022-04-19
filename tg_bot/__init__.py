from email.message import EmailMessage
from .settings import Settings
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler
from .constants import (
    CART, CART_ORDER_CHECK_NUMBER, CART_ORDER_LOCATION, CART_ORDER_PASSPORT_IMAGE, CART_ORDER_SELF_IMAGE, CART_ORDER_SELF_PASSWORD_IMAGE, FILIAL, GET_NUMBER_FOR_ORDER, ORDER, OUR_ADDRESSES, SETTINGS, SETTINGS_LANGUAGE, SETTINGS_NAME, SETTINGS_NUMBER, SUPPORT, TOKEN, LANGUAGE, NAME, NUMBER,MENU
)
from .basehandlers import Basehandlers
from .order import Order

class Bot(Updater, Basehandlers, Order, Settings):
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
                ],
                FILIAL: [
                    MessageHandler(Filters.text, self.filial)
                ],
                MENU: [
                    MessageHandler(
                        Filters.regex(
                            ("^(" "Buyurtma berish" "|" "Заказать" "|" "Order" ")$")), self.order
                        ),
                    MessageHandler(Filters.regex("^Savatcha$"), self.cart),
                    MessageHandler(Filters.regex("^Telefon orqali aloqa$"), self.contact_with_phone),
                    MessageHandler(Filters.regex(
                        "^(Sozlamalar|Настройки)$"), self.settings),
                    MessageHandler(Filters.regex(
                        "^Bizning manzillar$"), self.our_addresses),
                        MessageHandler(Filters.regex("^(Savol va takliflar)$"), self.support),
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
                    MessageHandler(Filters.location, self.cart_order_location)
                ],
                CART_ORDER_SELF_IMAGE:[
                    MessageHandler(Filters.photo, self.cart_order_self_image)
                ],
                CART_ORDER_PASSPORT_IMAGE: [
                    MessageHandler(Filters.photo, self.cart_order_passport_image)
                ],
                CART_ORDER_SELF_PASSWORD_IMAGE: [
                    MessageHandler(Filters.photo, self.cart_order_self_password_image)
                ],
                CART_ORDER_CHECK_NUMBER: [
                    MessageHandler(
                        Filters.regex("^(✅|❌)"), self.cart_order_check_number
                    )
                ],
                GET_NUMBER_FOR_ORDER: [
                    MessageHandler(Filters.text, self.get_number_for_order)
                ],
                SETTINGS: [
                    MessageHandler(Filters.regex("^(Ismni o'zgartirish)$"), self.settings_name),
                    MessageHandler(Filters.regex("^(Tilni o'zgartirish)$"), self.settings_language),
                    MessageHandler(Filters.regex("^(Raqamni o'zgartirish)$"), self.settings_number),
                    MessageHandler(Filters.regex("^Ortga$"), self.back_to_menu)
                ],
                SETTINGS_NAME: [
                    MessageHandler(Filters.text, self.settings_name_change)
                ],
                SETTINGS_NUMBER: [
                    MessageHandler(Filters.contact, self.settings_number_change),
                    MessageHandler(Filters.regex(
                        "(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})") | Filters.regex(
                        "(?:[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"), self.settings_number_text),
                    MessageHandler(Filters.text, self.settings_number_error)
                ],
                SETTINGS_LANGUAGE: [
                    MessageHandler(Filters.text, self.settings_language_change)
                ],
                OUR_ADDRESSES: [
                    CallbackQueryHandler(self.address, pattern="^address:"),
                    CallbackQueryHandler(
                        self.our_addresses, pattern="^back_to_our_addresses"),
                    CallbackQueryHandler(
                        self.back_to_menu, pattern="^back_to_menu_from_our_addresses"),
                ],
                SUPPORT: [
                    MessageHandler(Filters.text, self.support_message)
                ]

            },
            [
                CommandHandler('start', self.start),
            ]
        )
        

        self.dispatcher.add_handler(self.conversation)


        self.start_polling()
        print(self.bot.get_me())
        self.idle(  )