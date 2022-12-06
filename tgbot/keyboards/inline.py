import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_btn1 = InlineKeyboardButton("Кэжуал", callback_data="casual")
inline_btn2 = InlineKeyboardButton("Стритвер", callback_data="streetwear")
inline_btn3 = InlineKeyboardButton("Винтаж", callback_data="vintage")
inline_kb_styles = InlineKeyboardMarkup().add(inline_btn1, inline_btn2, inline_btn3)

inline_btn4 = InlineKeyboardButton("5 вещей", callback_data="5")
inline_btn5 = InlineKeyboardButton("8 вещей", callback_data="8")
inline_btn6 = InlineKeyboardButton("12 вещей", callback_data="12")
inline_kb_capsule_size = InlineKeyboardMarkup().add(inline_btn4, inline_btn5, inline_btn6)

inline_btn7 = InlineKeyboardButton("Мужской", callback_data="man")
inline_btn8 = InlineKeyboardButton("Женский", callback_data="woman")
inline_kb_gender = InlineKeyboardMarkup().add(inline_btn7, inline_btn8)


async def create_inline_kb_date_delivery():
    today: datetime = datetime.date.today()
    keyboard = InlineKeyboardMarkup()
    for i in range(1, 4):
        delta = datetime.timedelta(hours=24)
        date = today + delta * i
        day = str(date.day) if date.day > 9 else '0' + str(date.day)
        keyboard.add(InlineKeyboardButton(str(date.month) + "." + day,
                                          callback_data=str(date.month) + "." + day))
    return keyboard

async def create_inline_kb_time_delivery():
    keyboard = InlineKeyboardMarkup(row_width=4)
    deliveryTime = set()
    time = datetime.timedelta(hours=12)
    delta = datetime.timedelta(minutes=30)
    for i in range(20):
        newTime = time + delta * i
        tsec = newTime.total_seconds()
        hour = str(int(tsec / (60*60)))
        minute = '0' + str(int(tsec / 60 % 60)) if tsec / 60 % 60 == 0 else str(int(tsec / 60 % 60))
        deliveryTime.add(hour + ":" + minute)
    # запрос занятых вермен для доставки
    # вычитание множеств
    deliveryTime = list(deliveryTime)
    deliveryTime.sort()
    for time in deliveryTime:
        keyboard.insert(InlineKeyboardButton(time, callback_data=time))
    return keyboard


async def create_inline_kb_sizes(style: str, capsule_size: str):
    # запрос доступных размеров одежды в капсулах определенного стиля и размера
    keyboard = InlineKeyboardMarkup(row_width=2)
    constSizes = ["XS", "S", "M", "l", "XL"]
    sizesM = ["M", "l", "XL"]
    sizesW = ["S", "M", "L"]
    iterM = iter(sizesM)
    iterW = iter(sizesW)
    i = 0
    while i < len(constSizes):
        sizeM = next(iterM)
        sizeW = next(iterW)
        if sizeM != constSizes[i]:
            sizesM.insert(i, "-")
        if sizeW != constSizes[i]:
            sizesW.insert(i, "-")
        i += 1


    sizesMres = ["XS", "-", "M", "l", "XL"]
    sizesWres = ["-", "S", "M", "L", "-"]
    keyboard.row(InlineKeyboardButton("Мужские размеры", callback_data="мужские"),
                 InlineKeyboardButton("Женские размеры", callback_data="женские"))
    # i = 0
    # iterM = iter(sizesM)
    # iterW = iter(sizesW)
    # while i < max(len(sizesM), len(sizesW)):
    #     sizeM = next(iterM)
    #     sizeW = next(iterW)
    #     if sizeM != sizeW
    #
    #
    #
    #
    #
    #
    # while (i < max(len(sizesM), len(sizesW))):
    #     if sizesW[i] == sizesM[i]:
    #         keyboard.row(InlineKeyboardButton(sizesM[i], callback_data="m" + sizesM[i]),
    #                      InlineKeyboardButton(sizesW[i], callback_data="w" + sizesW[i]))
    #     else:
    #
    #     i += 1
    for size in sizesM:
        keyboard.row(InlineKeyboardButton(size, callback_data="m" + size),
                     InlineKeyboardButton(size, callback_data="w" + size))
    keyboard.row(InlineKeyboardButton("XL", callback_data="m" + "XL"),
                 InlineKeyboardButton("-", callback_data="-"))
    return keyboard
