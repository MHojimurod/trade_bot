from telegram import *
from telegram.ext import *
from admin_panel.models import Language, distribute
from tg_bot.constants import SETTINGS, SETTINGS_LANGUAGE, SETTINGS_NAME, SETTINGS_NUMBER

from tg_bot.utils import get_user


class Settings:
    def settings(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        user.send_message("Settings", reply_markup=ReplyKeyboardMarkup(
            [
                [
                    "Ismni o'zgartirish",
                    "Tilni o'zgartirish",
                    "Raqamni o'zgartirish",
                ]
            ],True
        ))
        return SETTINGS
    
    def settings_name(self, update:Update, context: CallbackContext):
        user, db=  get_user(update)
        user.send_message("Iltimos yangi ismingizni kiriting!", reply_markup=ReplyKeyboardRemove())
        return SETTINGS_NAME
    
    def settings_name_change(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        db.name = update.message.text
        db.save()
        user.send_message("Ism o'zgartirildi!", reply_markup=ReplyKeyboardMarkup(
            [
                [
                    "Ismni o'zgartirish",
                    "Tilni o'zgartirish",
                    "Raqamni o'zgartirish",
                ]
            ], True
        ))
        return SETTINGS


    def settings_language(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        user.send_message("Iltimos yangi tilni kiriting!", reply_markup=ReplyKeyboardMarkup(
            distribute(
                [
                    l.name for l in Language.objects.all()
                ],
                2
            )
        ))
        return SETTINGS_LANGUAGE
    

    

    def settings_language_change(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        lang = Language.objects.filter(name=update.message.text).first()
        if lang:
            db.language = lang
            db.save()
            user.send_message("Til o'zgartirildi!", reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        "Ismni o'zgartirish",
                        "Tilni o'zgartirish",
                        "Raqamni o'zgartirish",
                    ]
                ],True
            ))
            return SETTINGS
        else:
            user.send_message("Til topilmadi!", reply_markup=ReplyKeyboardMarkup(
                distribute(
                    [
                        l.name for l in Language.objects.all()
                    ],
                    2
                )
            ))
            SETTINGS_LANGUAGE
        
    
    def settings_number(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        user.send_message("Iltimos yangi raqamni kiriting!", reply_markup=ReplyKeyboardMarkup([
            [
                KeyboardButton("Raqamni yuborish", request_contact=True)
            ]
        ]))
        return SETTINGS_NUMBER
    
    def settings_number_change(self, update: Update, context: CallbackContext):
        user, db = get_user(update)
        db.number = update.message.contact.phone_number
        db.save()
        user.send_message("Raqam o'zgartirildi!", reply_markup=ReplyKeyboardMarkup(
            [
                [
                    "Ismni o'zgartirish",
                    "Tilni o'zgartirish",
                    "Raqamni o'zgartirish",
                ]
            ],True
        ))
        return SETTINGS
    
