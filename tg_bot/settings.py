from token import NUMBER
from telegram import *
from telegram.ext import *
from admin_panel.models import Fillials, Language, distribute
from tg_bot.constants import SETTINGS, SETTINGS_FILIAL, SETTINGS_LANGUAGE, SETTINGS_NAME, SETTINGS_NUMBER

from tg_bot.utils import get_user


class Settings:
    def settings(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        user.send_message(db.text("settings_info", _name=db.name, number=db.number, lang=f"{db.language.name} ({db.language.code})"), reply_markup=ReplyKeyboardMarkup(
            db.settings,True
        ), parse_mode="HTML")
        return SETTINGS
    
    def settings_name(self, update:Update, context: CallbackContext):
        user, db=  get_user(update)
        user.send_message("Iltimos yangi ismingizni kiriting!", reply_markup=ReplyKeyboardMarkup(
            [
                [
                    db.text("back")
                ]
            ],
            True
        ))
        return SETTINGS_NAME
    
    def settings_name_change(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        if len(update.message.text.split()) >= 2:
            db.name = update.message.text
            db.save()
            user.send_message("Ism o'zgartirildi!", reply_markup=ReplyKeyboardMarkup(
                db.settings, True
            ))
            self.settings(update, context)
            return SETTINGS
        else:
            user.send_message("Iltimos ismni to'g'ri kiriting!", reply_markup=ReplyKeyboardRemove())
            return SETTINGS_NAME


    def settings_language(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        user.send_message("Iltimos yangi tilni kiriting!", reply_markup=ReplyKeyboardMarkup(
            [*distribute(
                [
                    l.name for l in Language.objects.all()
                ],
                2
            ), [
                    db.text("back")
                ]],True
        ))
        return SETTINGS_LANGUAGE
    

    

    def settings_language_change(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        lang = Language.objects.filter(name=update.message.text).first()
        if lang:
            db.language = lang
            db.save()
            user.send_message("Til o'zgartirildi!", reply_markup=ReplyKeyboardMarkup(
                db.settings,True
            ))
            self.settings(update, context)
            return SETTINGS
        else:
            user.send_message("Til topilmadi!", reply_markup=ReplyKeyboardMarkup(
                [*distribute(
                    [
                        l.name for l in Language.objects.all()
                    ],
                    2
                ), [
                    db.text("back")
                ]],
                True
            ))
            SETTINGS_LANGUAGE
        
    
    def settings_number(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        user.send_message("Iltimos yangi raqamni kiriting!", reply_markup=ReplyKeyboardMarkup([
            [
                KeyboardButton("Raqamni yuborish", request_contact=True)
            ],
            [
                    db.text("back")
                ]
        ], True))
        return SETTINGS_NUMBER
    
    def settings_number_change(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        db.number = update.message.contact.phone_number
        db.save()
        user.send_message("Raqam o'zgartirildi!", reply_markup=ReplyKeyboardMarkup(
            
                db.settings
            ,True
        ))
        self.settings(update, context)
        return SETTINGS
    
    def settings_number_text(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        db.number = update.message.text
        db.save()
        user.send_message("Raqam o'zgartirildi!", reply_markup=ReplyKeyboardMarkup(
            db.settings,True
        ))
        self.settings(update, context)
        return SETTINGS
    
    def settings_number_error(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        user.send_message("Iltimos raqamni to'g'ri yuboring!", reply_markup=ReplyKeyboardMarkup([
            [
                KeyboardButton("Raqamni yuborish", request_contact=True)
            ]
        ], True))
        return SETTINGS_NUMBER
    
    def number_error(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        user.send_message("Iltimos raqamni to'g'ri yuboring!", reply_markup=ReplyKeyboardMarkup([
            [
                KeyboardButton("Raqamni yuborish", request_contact=True)
            ]
        ], True))
        return NUMBER
    
    def settings_change_filial(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        user.send_message(db.text("select_filial"), reply_markup=ReplyKeyboardMarkup(distribute([
            f.name(context.user_data['register']['language']) for f in Fillials.objects.filter(active=True)
        ], 2)), parse_mode="HTML")
        return SETTINGS_FILIAL
    
    def settings_change_filial_change(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        filial = Fillials.objects.filter(name=update.message.text).first()
        if filial:
            db.filial = filial
            db.save()
            user.send_message(db.text("filial_changed"), reply_markup=ReplyKeyboardMarkup(db.settings, True), parse_mode="HTML")
            self.settings(update, context)
            return SETTINGS
        else:
            user.send_message(db.text("filial_not_found"), reply_markup=ReplyKeyboardMarkup(db.settings, True), parse_mode="HTML")
            self.settings_change_filial(update, context)
            return SETTINGS_FILIAL