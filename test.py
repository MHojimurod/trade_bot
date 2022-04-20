import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def money(number: int, grouping: bool = True, lang=1):
    return f"{locale.currency(number, grouping=grouping).split('.')[0][1:]}"


print(money(1_000_000, grouping=True))