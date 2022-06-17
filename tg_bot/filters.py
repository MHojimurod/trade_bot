from telegram import Update, Message
from telegram.ext import MessageHandler,Filters, MessageFilter

from tg_bot.utils import get_user
from admin_panel.models import User



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


class MultiLanguageFilter(MessageFilter):
    def __init__(self, textName):
        self.textName = textName
    
    def filter(self, message:Message):
        if message.text:
            user:User = User.objects.filter(chat_id=message.from_user.id).first()
            return user and (user.text(self.textName) == message.text)