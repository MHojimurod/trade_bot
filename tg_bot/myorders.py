

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
                per_month = 0
                total = 0
                order: Busket = orders[0]
                text = ""
                product: BusketItem
                for product in order.products:
                    text += """{pr_name}
    {per_month} x {month} {month_text} x {count} ta = {price} {money}\n""".format(
                    pr_name=product.product.name(db.language),
                    per_month=product.product.price(product.month) // product.month.months,
                    month=product.month.months,
                    month_text=db.language.month(),
                    count=product.count,
                    price=product.product.price(product.month) // product.month.months * product.count,
                    money=db.language.money()
      )
                    per_month += product.product.price(product.month) // product.month.months
                    total += product.product.price(product.month) * product.count
                controls = []


                if len(orders) > 1:
                    controls.append(
                        [
                        InlineKeyboardButton("➡️", callback_data=f"my_orders:{1}")
                        ]
                    )
                controls.append([
                    InlineKeyboardButton(db.text('back'), callback_data="back_to_menu")
                ])
                text += {
                    "uz": f"""Bir oylik to'lov: {per_month} so'm
Umumiy narx: {total} so'm""",
                    "ru": f"""Ежемесячная плата: {per_month} руб.
Общая сумма: {total} руб.""",
                    "en": f"""Monthly payment: {per_month} rub.
Total amount: {total} rub."""
                }[db.language.code]
                
                update.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(controls))
                return MY_ORDERS
            else:
                update.message.reply_text(db.text("no_orders"))
            

        elif update.callback_query:
            index = int(update.callback_query.data.split(":")[1])
            orders = db.get_orders()
            if orders:
                order: Busket = orders[index]
                text = ""
                product: BusketItem
                for product in order.products:
                    text += db.text("my_orders_order_text_one_line",
                    pr_name=product.product.name(db.language),
                    price_per_month=product.product.price(product.month) // product.month.months,
                    months=product.month.months,
                    price=product.product.price(product.month),

                    total_price_per_month=product.product.price(product.month) // product.month.months,
                    count=product.count,
                    total_price=product.product.price(product.month) // product.month.months * product.count
                    )
                    # text += f"""<b>{product.product.name(db.language)}</b>\n    • {product.product.price(product.month) // product.month.months} x {product.month.months} = {product.product.price(product.month)}\numumiy narxi\n    • {product.product.price(product.month) // product.month.months} x {product.count} = {product.product.price(product.month) //  product.month.months * product.count}\n\n"""
                    # text += """<b>{pr_name}</b>\n    • {price_per_month} x {months} = {price}\numumiy narxi\n    • {total_price_per_month} x {count} = {total_price}\n\n"""

                controls = []
                cont = []
                if index > 0:
                    cont.append(
                        
                        InlineKeyboardButton("⬅️", callback_data=f"my_orders:{index -1}")
                        
                    )
                if index < len(orders) - 1:
                    cont.append(
                        
                        InlineKeyboardButton("➡️", callback_data=f"my_orders:{index + 1}")
                        
                    )
                controls.append(cont)
                controls.append([
                    InlineKeyboardButton(db.text('back'), callback_data="back_to_menu")
                ])
                
                update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(controls))

            else:
                update.message.reply_text(db.text("no_orders"))