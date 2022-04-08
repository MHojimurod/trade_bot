from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
from .constants import (
    TOKEN, LANGUAGE, NAME, NUMBER,MENU
)
from .basehandlers import Basehandlers

class Bot(Updater, Basehandlers):
    def __init__(self,*args, **kwargs):

        super().__init__(TOKEN, *args, **kwargs)


        self.conversation = ConversationHandler(
            [
                CommandHandler('start', self.start),
            ],
            {
                LANGUAGE: [
                    MessageHandler(Filters.text, self.language),
                ],
                NAME: [
                    MessageHandler(Filters.text, self.name),
                ],
                NUMBER: [
                    MessageHandler(Filters.contact, self.number),
                ],
                MENU: [
                    
                ]

            },
            [
                CommandHandler('start', self.start),
            ]
        )
        

        self.dispatcher.add_handler(self.conversation)


        self.start_polling()
        self.idle(  )