

from math import prod
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from admin_panel.models import Busket, BusketItem, money
from tg_bot.constants import MENU, MY_ORDERS

from tg_bot.utils import get_user, remove_temp_message

class myOrders:
    @remove_temp_message
    def my_orders(self, update: Update, context:CallbackContext):
        user, db = get_user(update)
        if update.message:
            context.user_data['my_orders_page'] = 0
            orders = db.get_orders()
            if orders:
                per_month_total = 0
                total = 0
                order: Busket = orders[0]
                text = ""
                product: BusketItem

                for product in order.products:
                    product: BusketItem
                    text += """{pr_name}\n    {one_product_per_month} {money} x {month} {month_word} x {count} {count_word} = {total}\n""".format(
                        pr_name=product.product.name(db.language),
                        one_product_per_month=money(product.product.price(product.month) // product.month.months),
                        month=product.month.months,
                        count=product.count,
                        total = money(product.product.price(product.month) * product.count),
                        money=db.language.money(),
                        month_word=db.language.month(),
                        count_word={
                            "uz": "ta",
                            "ru": "ัััะบ",
                            "en": "piece"
                        }[db.language.code])
                    per_month_total += (product.product.price(product.month) // product.month.months) * product.count
                    total += product.product.price(product.month) * product.count
                
                # text += f"""\n\nBir oylik to'lov: {per_month_total}\nUmumiy narx: {total}"""
                per_month_total = money(per_month_total)
                total = money(total)
                text += {
                    "uz": f"""Bir oylik to'lov: {per_month_total} so'm
Umumiy narx: {total} so'm""",
                    "ru": f"""ะะถะตะผะตัััะฝะฐั ะฟะปะฐัะฐ: {per_month_total} ััะผ.
ะะฑัะฐั ััะผะผะฐ: {total} ััะผ.""",
                    "en": f"""Monthly payment: {per_month_total} sums.
Total amount: {total} sums."""
                }[db.language.code]
                controls = []

                if len(orders) > 1:
                    controls.append([InlineKeyboardButton("โก๏ธ", callback_data="my_orders:1")])
                
                controls.append([InlineKeyboardButton(db.text('back'), callback_data="back_to_menu")])
                user.send_message(text, reply_markup=InlineKeyboardMarkup(controls))
                return MY_ORDERS
            else:
                update.message.reply_text(db.text("no_orders"))
        elif update.callback_query:
            
            index = int(update.callback_query.data.split(":")[1])
            orders = db.get_orders()
            if orders:
                per_month_total = 0
                total = 0
                order: Busket = orders[index]
                text = ""
                product: BusketItem
                for product in order.products:
                    text += """{pr_name}\n    {one_product_per_month} {money} x {month} {month_word} x {count} {count_word} = {total}\n""".format(
                        pr_name=product.product.name(db.language),
                        one_product_per_month=money(product.product.price(product.month) // product.month.months),
                        month=product.month.months,
                        count=product.count,
                        total = money(product.product.price(product.month) * product.count),
                        money=db.language.money(),
                        month_word=db.language.month(),
                        count_word={
                            "uz": "ta",
                            "ru": "ัััะบ",
                            "en": "piece"
                        }[db.language.code])
                    per_month_total += (product.product.price(product.month) // product.month.months) * product.count
                    total += product.product.price(product.month) * product.count
                per_month_total = money(per_month_total)
                total = money(total)
                text += {
                    "uz": f"""Bir oylik to'lov: {per_month_total} so'm
Umumiy narx: {total} so'm""",
                    "ru": f"""ะะถะตะผะตัััะฝะฐั ะฟะปะฐัะฐ: {per_month_total} ััะผ.
ะะฑัะฐั ััะผะผะฐ: {total} ััะผ.""",
                    "en": f"""Monthly payment: {per_month_total} sums.
Total amount: {total} sums."""
                }[db.language.code]

                controls = []
                cont = []
                if index > 0:
                    cont.append(
                        
                        InlineKeyboardButton("โฌ๏ธ", callback_data=f"my_orders:{index -1}")
                    )
                if index < len(orders) - 1:
                    cont.append(
                        InlineKeyboardButton("โก๏ธ", callback_data=f"my_orders:{index + 1}")
                    )
                controls.append(cont)

                controls.append([
                    InlineKeyboardButton(db.text('back'), callback_data="back_to_menu")
                ])
                
                update.callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(controls))
        else:
                update.message.reply_text(db.text("no_orders"))
            

#         if update.message:
#             context.user_data['my_orders_page'] = 0

#             orders = db.get_orders()
#             if orders:
#                 per_month = 0
#                 total = 0
#                 order: Busket = orders[0]
#                 text = ""
#                 product: BusketItem
                
#                 for product in order.products:
#                     text += """{pr_name}
#     {per_month} x {month} {month_text} x {count} ta = {price} {money}\n""".format(
#                     pr_name=product.product.name(db.language),
#                     per_month=product.product.price(product.month) // product.month.months * product.count,
#                     month=product.month.months,
#                     month_text=db.language.month(),
#                     count=product.count,
#                     price=((product.product.price(product.month) // product.month.months) * product.count) * product.month.months,
#                     money=db.language.money()
#       )
#                     per_month += product.product.price(product.month) // product.month.months
#                     total += product.product.price(product.month) * product.count
#                 controls = []


#                 if len(orders) > 1:
#                     controls.append(
#                         [
#                         InlineKeyboardButton("โก๏ธ", callback_data=f"my_orders:{1}")
#                         ]
#                     )
#                 controls.append([
#                     InlineKeyboardButton(db.text('back'), callback_data="back_to_menu")
#                 ])
#                 text += {
#                     "uz": f"""Bir oylik to'lov: {per_month} so'm
# Umumiy narx: {total} so'm""",
#                     "ru": f"""ะะถะตะผะตัััะฝะฐั ะฟะปะฐัะฐ: {per_month} ััะฑ.
# ะะฑัะฐั ััะผะผะฐ: {total} ััะฑ.""",
#                     "en": f"""Monthly payment: {per_month} rub.
# Total amount: {total} rub."""
#                 }[db.language.code]
                
#                 update.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(controls))
#                 return MY_ORDERS
#             else:
#                 update.message.reply_text(db.text("no_orders"))
            

#         elif update.callback_query:
#             index = int(update.callback_query.data.split(":")[1])
#             orders = db.get_orders()
#             if orders:
#                 order: Busket = orders[index]
#                 text = ""
#                 product: BusketItem
#                 for product in order.products:
#                     text += db.text("my_orders_order_text_one_line",
#                     pr_name=product.product.name(db.language),
#                     price_per_month=product.product.price(product.month) // product.month.months,
#                     months=product.month.months,
#                     price=product.product.price(product.month),

#                     total_price_per_month=product.product.price(product.month) // product.month.months,
#                     count=product.count,
#                     total_price=product.product.price(product.month) // product.month.months * product.count
#                     )
#                     # text += f"""<b>{product.product.name(db.language)}</b>\n    โข {product.product.price(product.month) // product.month.months} x {product.month.months} = {product.product.price(product.month)}\numumiy narxi\n    โข {product.product.price(product.month) // product.month.months} x {product.count} = {product.product.price(product.month) //  product.month.months * product.count}\n\n"""
#                     # text += """<b>{pr_name}</b>\n    โข {price_per_month} x {months} = {price}\numumiy narxi\n    โข {total_price_per_month} x {count} = {total_price}\n\n"""

#                 controls = []
#                 cont = []
#                 if index > 0:
#                     cont.append(
                        
#                         InlineKeyboardButton("โฌ๏ธ", callback_data=f"my_orders:{index -1}")
                        
#                     )
#                 if index < len(orders) - 1:
#                     cont.append(
                        
#                         InlineKeyboardButton("โก๏ธ", callback_data=f"my_orders:{index + 1}")
                        
#                     )
#                 controls.append(cont)
#                 controls.append([
#                     InlineKeyboardButton(db.text('back'), callback_data="back_to_menu")
#                 ])
                
#                 update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(controls))

#             else:
#                 update.message.reply_text(db.text("no_orders"))