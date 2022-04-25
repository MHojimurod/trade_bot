

from math import prod
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from admin_panel.models import Busket, BusketItem
from tg_bot.constants import MENU, MY_ORDERS

from tg_bot.utils import get_user

class myOrders:
    def my_orders(self, update: Update, context:CallbackContext):
        user, db = get_user(update)
        if update.message:
            context.user_data['my_orders_page'] = 0
            orders = db.get_orders()
            if orders:
                order: Busket = orders.first()
                # if not order.is_ordered:
                #     update.message.reply_text("Sizning buyurtmalarimiz yo'q")
                #     return MENU
                text = ""
                product: BusketItem
                for product in order.products:
                    text += f"""<b>{product.product.name(db.language)}</b>\n    • {product.product.price(product.month) // product.month.months} x {product.month.months} = {product.product.price(product.month)}\numumiy narxi\n    • {product.product.price(product.month) // product.month.months} x {product.count} = {product.product.price(product.month) //  product.month.months * product.count}\n\n"""
                controls = []
                if orders.count() > 1:
                    controls.append(
                        [
                        InlineKeyboardButton("➡️", callback_data=f"my_orders:{1}")
                        ]
                    )
                controls.append([
                    InlineKeyboardButton(db.text('back'), callback_data="back_to_menu")
                ])
                
                update.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(controls))
                return MY_ORDERS
            else:
                update.message.reply_text("Sizning buyurtmalarimiz yo'q")
            

        elif update.callback_query:
            index = int(update.callback_query.data.split(":")[1])
            orders = db.get_orders()
            if orders:
                order: Busket = orders[index]
                text = ""
                product: BusketItem
                for product in order.products:
                    text += f"""<b>{product.product.name(db.language)}</b>\n    • {product.product.price(product.month) // product.month.months} x {product.month.months} = {product.product.price(product.month)}\numumiy narxi\n    • {product.product.price(product.month) // product.month.months} x {product.count} = {product.product.price(product.month) //  product.month.months * product.count}\n\n"""
                controls = []
                cont = []
                if index > 0:
                    cont.append(
                        
                        InlineKeyboardButton("⬅️", callback_data=f"my_orders:{index -1}")
                        
                    )
                print(index, orders.count())
                if index < orders.count() - 1:
                    cont.append(
                        
                        InlineKeyboardButton("➡️", callback_data=f"my_orders:{index + 1}")
                        
                    )
                controls.append(cont)
                controls.append([
                    InlineKeyboardButton(db.text('back'), callback_data="back_to_menu")
                ])
                
                update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(controls))

            else:
                update.message.reply_text("Sizning buyurtmalarimiz yo'q")