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
                        self.category_list, pattern="^category_list:")
                 ]

            },
            [
                CommandHandler('start', self.start),
            ]
        )
        

        self.dispatcher.add_handler(self.conversation)


        self.start_polling()
        self.idle(  )