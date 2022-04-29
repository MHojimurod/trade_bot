from telegram import Update
from telegram.ext import MessageHandler,Filters

from tg_bot.utils import get_user



class MultilanguageMessageHandler(MessageHandler):
    def __init__(self, textName, callback, **kwargs):
        self.textName = textName
        self.filters = Filters.update & Filters.text
        self.run_async = True
        self.callback = callback


    def check_update(self, update):
        if isinstance(update, Update) and update.effective_message:
            user, db = get_user(update)
            res = db.text(self.textName) == update.effective_message.text
            print(res, "|", db.text(self.textName), "|" , update.effective_message.text, self.textName)
            return res
        return None