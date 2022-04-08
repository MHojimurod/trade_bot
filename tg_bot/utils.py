



from telegram import Update, User as tgUser
from admin_panel.models import User
from telegram import ReplyKeyboardMarkup as x


def get_user(update: Update) -> "tuple[tgUser, User]":
    user = update.message.from_user if update.message else update.callback_query.from_user
    
    return (user,
        User.objects.filter(chat_id=user.id).first()
    )


def is_odd(a):
    return bool(a - ((a >> 1) << 1))


def distribute(items, number) -> list:
    res = [  ]
    start = 0
    end = number
    for item in items:
        if items[start:end] == []:
            return res
        res.append(items[start:end])
        start += number
        end += number
    return res


class ReplyKeyboardMarkup(x):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.resize_keyboard = True