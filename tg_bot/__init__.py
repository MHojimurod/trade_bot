from email.message import Message
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler
from .constants import (
    CART, CART_ORDER_CHECK_NUMBER, CART_ORDER_LOCATION, CART_ORDER_PASSPORT_IMAGE, CART_ORDER_SELF_IMAGE, CART_ORDER_SELF_PASSWORD_IMAGE, GET_NUMBER_FOR_ORDER, ORDER, TOKEN, LANGUAGE, NAME, NUMBER,MENU
)
from .basehandlers import Basehandlers
from .order import Order

class Bot(Updater, Basehandlers, Order):
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
                MENU: [
                    MessageHandler(
                        Filters.regex(
                            ("^(" "Buyurtma berish" "|" "заказать " "|" "Order" ")$") ), self.order
                        ),
                    MessageHandler(Filters.regex("^Savatcha$"), self.cart),
                    MessageHandler(Filters.regex("^Telefon orqali aloqa$"), self.contact_with_phone)
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
                        self.cart_product_count, pattern="^cart_product_count:"),
                    
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
                ]

            },
            [
                CommandHandler('start', self.start),
            ]
        )
        

        self.dispatcher.add_handler(self.conversation)


        self.start_polling()
        self.idle(  )