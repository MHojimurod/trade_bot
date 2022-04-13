from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler
from .constants import (
    ORDER, TOKEN, LANGUAGE, NAME, NUMBER,MENU
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
                        )
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
                        self.add_to_cart, pattern="add_to_cart"),
                    CallbackQueryHandler(
                        self.cart, pattern="^cart"),
                 ]

            },
            [
                CommandHandler('start', self.start),
            ]
        )
        

        self.dispatcher.add_handler(self.conversation)


        self.start_polling()
        self.idle(  )