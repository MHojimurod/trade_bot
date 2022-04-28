from telegram.ext import CallbackContext, Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from admin_panel.models import Aksiya, Language, Support, User, Fillials
from telegram import User as tgUser
from tg_bot.utils import distribute, get_user
from .constants import  ADDRESS, AKSIYA, FILIAL, LANGUAGE, NAME, NUMBER, MENU, OUR_ADDRESSES, SUPPORT


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
            ), parse_mode="HTML")
            return LANGUAGE
        else:
            context.user_data['temp_message'] = user.send_message(
                db.text("mainMenu"), reply_markup=ReplyKeyboardMarkup(db.menu()), parse_mode="HTML")
            return MENU
    
    @remove_temp_message
    def language(self, update:Update, context: CallbackContext):
        user,db = get_user(update)
        language = update.message.text
        lang:Language = Language.objects.filter(name=language).first()


        if lang:
            context.user_data['register']['language'] = lang
            context.user_data['temp_message'] = user.send_message(
                lang._("send_name_and_surname"), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
            return NAME
        else:
            context.user_data['temp_message'] = user.send_message(
                "Til topilmadi!", parse_mode="HTML")

    @remove_temp_message
    def name(self, update:Update, context:CallbackContext):
        user,db = get_user(update)
        name = update.message.text
        lang:Language = context.user_data['register']['language']
        if len(name.split()) >= 2:
            context.user_data['register']['name'] = name
            context.user_data['temp_message'] = user.send_message( lang._("send_number_register"), reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(lang._("send_number_register_button"), request_contact=True)
                    ]
                ]
            ), parse_mode="HTML")
            return NUMBER
        else:
            context.user_data['temp_message'] = user.send_message(
                lang._("name_error"), parse_mode="HTML")
            return NAME

    @remove_temp_message
    def number(self, update:Update, context:CallbackContext):
        user,db = get_user(update)
        number = update.message.contact.phone_number if update.message.contact else update.message.text
        context.user_data['register']['number'] = number
        filials: list[Fillials] = Fillials.objects.filter(active=True)
        lang:Language = context.user_data['register']['language']
        user.send_message(lang._("select_filial"), reply_markup=ReplyKeyboardMarkup(distribute([
            f.name(context.user_data['register']['language']) for f in filials
        ], 2)), parse_mode="HTML")

        return FILIAL
    
    def filial(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        filial = Fillials.objects.filter(**{
            "name_" + context.user_data['register']['language'].code: update.message.text
        })
        lang: Language = context.user_data['register']['language']
        if filial:
            context.user_data['register']['filial'] = filial.first()
            new_user: User = User.objects.create(**context.user_data['register'])
            user.send_message(new_user.text('successfully_registered'),
                              reply_markup=ReplyKeyboardMarkup(new_user.menu()), parse_mode="HTML")
        else:
            filials: list[Fillials] = Fillials.objects.filter(active=True)
            user.send_message(lang._("filial_not_found"), reply_markup=ReplyKeyboardMarkup(distribute([
                f.name(context.user_data['register']['language']) for f in filials
            ], 2)), parse_mode="HTML")
            return FILIAL
        return MENU
    
    def contact_with_phone(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        user.send_message(db.text('contact_with_phone'), parse_mode="HTML")
    
    def our_addresses(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        text = f"{db.text('our_addresses')}\n"
        keyboard = []
        address: Fillials
        for address in Fillials.objects.all():
            keyboard.append(address.name(db.language))
                
        
        user.send_message(text=text, reply_markup=ReplyKeyboardMarkup([*distribute(keyboard,2), [ "🔙" +db.text("back")]
                                                                       ]), parse_mode="HTML")
        return OUR_ADDRESSES
    
    def address(self, update:Update, context:CallbackContext):
        user, db = get_user(update)
        address: Fillials = Fillials.objects.filter(
            **{
                "name_" + db.language.code: update.message.text
            }
        ).first()
        if address:
            user.send_message(address.address(db.language), parse_mode="HTML")
            return OUR_ADDRESSES
        else:
            keyboard = []
            address: Fillials
            for address in Fillials.objects.all():
                keyboard.append(address.name(db.language))
            user.send_message(text=db.text("address_not_found"), reply_markup=ReplyKeyboardMarkup([*distribute(keyboard, 2), [db.text("Orqaga")]
                                                                                                     ]), parse_mode="HTML")
            return OUR_ADDRESSES

    
    def support(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        user.send_message(db.text('support'),
                          reply_markup=ReplyKeyboardMarkup([
                              [
                                 db.text("back")
                              ]
                          ]), parse_mode="HTML")
        return SUPPORT
    
    def support_message(self, update:Update, context: CallbackContext):
        user, db = get_user(update)
        Support.objects.create(user=db, data=update.message.text)
        user.send_message(db.text('support_accepted'),
                          reply_markup=ReplyKeyboardMarkup(db.menu()))
        return MENU
    @remove_temp_message
    def aksiya(self, update: Update,context: CallbackContext):
        user, db = get_user(update)

        context.user_data['temp_message'] = user.send_message(db.text('offers'), reply_markup=ReplyKeyboardMarkup(
            [*distribute(Aksiya.keyboard(db.language), 2), [db.text("back")]]), parse_mode="HTML")
        return AKSIYA

    @remove_temp_message
    def aksiya_select(self, update: Update, context: CallbackContext):
        user, db = get_user(update)

        aksiya:Aksiya = Aksiya.objects.filter(**{
            "name_" + db.language.code: update.message.text
        }).first()

        if aksiya:
            if aksiya.mode == 0:
                context.user_data['temp_message'] = user.send_message(aksiya.caption, reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(db.text("back"), callback_data="back_to_aksiyas")]]), parse_mode="HTML")
            elif aksiya.mode == 1:
                context.user_data['temp_message'] = user.send_photo(photo=aksiya.file, caption=aksiya.caption, reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(db.text("back"), callback_data="back_to_aksiyas")]]), parse_mode="HTML")
                
            elif aksiya.mode == 2:
                context.user_data['temp_message'] = user.send_video(video=aksiya.file, caption=aksiya.caption, reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(db.text("back"), callback_data="back_to_aksiyas")]]))
        else:
            context.user_data['temp_message'] = user.send_message("Kechirasiz aksiya topilmadi!", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(db.text("back"), callback_data="back_to_aksiyas")]]), parse_mode="HTML")
            return AKSIYA

