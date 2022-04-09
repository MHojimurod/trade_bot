from telegram.ext import CallbackContext, Updater
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from admin_panel.models import Language, User
from telegram import User as tgUser
from tg_bot.utils import distribute, get_user
from .constants import  LANGUAGE, NAME, NUMBER, MENU

from .utils import *
class a(Update):
    pass


# class Basehandlers(a):
user: tgUser
db: User

class Basehandlers():
    def start(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        context.user_data['register'] = {
            "chat_id": user.id
        }
        if not db:
            user.send_message("Iltimos tilni tanlang!", reply_markup=ReplyKeyboardMarkup(
                distribute(
                    [
                        l.name for l in Language.objects.all()
                    ],
                    2
                )
            ))
            return LANGUAGE
        else:
            user.send_message("Salom", reply_markup=ReplyKeyboardMarkup(db.menu()))
            return MENU
    
    def language(self, update:Update, context: CallbackContext):
        user,db = get_user(update)
        language = update.message.text
        lang = Language.objects.filter(name=language).first()


        if lang:
            context.user_data['register']['language'] = lang
            user.send_message("Iltimos ismingizni va familyangizni kiriting!", reply_markup=ReplyKeyboardRemove())
            return NAME
        else:
            user.send_message("Til topilmadi!")
    
    def name(self, update:Update, context:CallbackContext):
        user,db = get_user(update)
        name = update.message.text
        if len(name.split()) >= 2:
            context.user_data['register']['name'] = name
            user.send_message("Iltimos telefon raqamingizni kiriting!", reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton('Send number', request_contact=True)
                    ]
                ]
            ))
            return NUMBER
        else:
            user.send_message("Iltimos ismingizni va familyangizni kiriting!")
            return NAME
        
    def number(self, update:Update, context:CallbackContext):
        user,db = get_user(update)
        number = update.message.contact.phone_number
        context.user_data['register']['number'] = number
        new_user: User = User.objects.create(**context.user_data['register'])

        user.send_message(
                          "Siz muvoffaqiyatli ro'yxatdan o'tdingiz!", reply_markup=ReplyKeyboardMarkup(new_user.menu()))
        return MENU