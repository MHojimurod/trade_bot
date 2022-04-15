from telegram.ext import CallbackContext, Updater
from telegram import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from admin_panel.models import Language, User, Fillials
from telegram import User as tgUser
from tg_bot.utils import distribute, get_user
from .constants import  LANGUAGE, NAME, NUMBER, MENU, OUR_ADDRESSES, SUPPORT


from .utils import *
class a(Update):
    pass


# class Basehandlers(a):
user: tgUser
db: User



class Basehandlers():
    def start(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        context.user_data['temp_message'] = None
        context.user_data['register'] = {
            "chat_id": user.id
        }
        if not db:
            context.user_data['temp_message'] = user.send_message("Iltimos tilni tanlang!", reply_markup=ReplyKeyboardMarkup(
                distribute(
                    [
                        l.name for l in Language.objects.all()
                    ],
                    2
                )
            ))
            return LANGUAGE
        else:
            context.user_data['temp_message'] = user.send_message(
                "Salom", reply_markup=ReplyKeyboardMarkup(db.menu()))
            return MENU
    
    @remove_temp_message
    def language(self, update:Update, context: CallbackContext):
        user,db = get_user(update)
        language = update.message.text
        lang = Language.objects.filter(name=language).first()


        if lang:
            context.user_data['register']['language'] = lang
            context.user_data['temp_message'] = user.send_message("Iltimos ismingizni va familyangizni kiriting!", reply_markup=ReplyKeyboardRemove())
            return NAME
        else:
            context.user_data['temp_message'] = user.send_message("Til topilmadi!")

    @remove_temp_message
    def name(self, update:Update, context:CallbackContext):
        user,db = get_user(update)
        name = update.message.text
        if len(name.split()) >= 2:
            context.user_data['register']['name'] = name
            context.user_data['temp_message'] = user.send_message("Iltimos telefon raqamingizni kiriting!", reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton('Send number', request_contact=True)
                    ]
                ]
            ))
            return NUMBER
        else:
            context.user_data['temp_message'] = user.send_message("Iltimos ismingizni va familyangizni kiriting!")
            return NAME

    @remove_temp_message
    def number(self, update:Update, context:CallbackContext):
        user,db = get_user(update)
        number = update.message.contact.phone_number
        context.user_data['register']['number'] = number
        new_user: User = User.objects.create(**context.user_data['register'])

        context.user_data['temp_message'] = user.send_message(
                          "Siz muvoffaqiyatli ro'yxatdan o'tdingiz!", reply_markup=ReplyKeyboardMarkup(new_user.menu()))
        return MENU
    
    def contact_with_phone(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        user.send_message("Bizning raqam bilan aloqa qiling!")
    
    def our_addresses(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        text = "Bizning manzillarimiz:\n"
        keyboard = []
        address: Fillials
        i = 1
        for address in Fillials.objects.all():
            text += f"{i}. {address.name(db.language)}"
            keyboard.append(InlineKeyboardButton(str(i), callback_data=f"address:{address.id}"))
            i += 1
        
        user.send_message(text=text, reply_markup=ReplyKeyboardMarkup(distribute(keyboard,5) + [[InlineKeyboardButton("Orqaga", callback_data="back_to_menu_from_our_addresses")]]))
        return OUR_ADDRESSES
    
    def address(self, update:Update, context:CallbackContext):
        address: Fillials = Fillials.objects.get(id=int(update.callback_query.data.split(":")[1]))
        user, db = get_user(update)
        user.send_message(address.address(db.language), reply_markup=InlineKeyboardButton("ortga", callback_data="back_to_our_addresses"))
    
    def support(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        user.send_message("Iltimos savol yoki taklifingizni yozing!", reply_markup=ReplyKeyboardRemove())
        return SUPPORT
    
    def support_message(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        user.send_message("Taklifingiz muvaffaqiyatli qabul qilindi!", reply_markup=ReplyKeyboardMarkup(*db.menu()))
        return MENU