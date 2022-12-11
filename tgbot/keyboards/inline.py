import datetime
import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.misc.api import api

inline_btn1 = InlineKeyboardButton("Винтаж", callback_data="vintage")
inline_btn3 = InlineKeyboardButton("Кэжуал", callback_data="casual")
inline_btn2 = InlineKeyboardButton("Стритвер", callback_data="streetwear")

inline_kb_styles = InlineKeyboardMarkup().add(inline_btn1, inline_btn2, inline_btn3)

inline_btn4 = InlineKeyboardButton("5 вещей", callback_data="5")
inline_btn5 = InlineKeyboardButton("8 вещей", callback_data="8")
inline_btn6 = InlineKeyboardButton("12 вещей", callback_data="12")
inline_kb_capsule_size = InlineKeyboardMarkup().add(inline_btn4, inline_btn5, inline_btn6)

inline_btn7 = InlineKeyboardButton("Мужской", callback_data="man")
inline_btn8 = InlineKeyboardButton("Женский", callback_data="woman")
inline_kb_gender = InlineKeyboardMarkup().add(inline_btn7, inline_btn8)

inline_btn9 = InlineKeyboardButton("Да", callback_data="yes")
inline_btn10 = InlineKeyboardButton("Нет", callback_data="no")
inline_kb_yes_no = InlineKeyboardMarkup().add(inline_btn9, inline_btn10)




logger = logging.getLogger(__name__)

async def create_inline_kb_accept(orderId):
    inline_btn = InlineKeyboardButton("Принять", callback_data=orderId)
    inline_kb_accept = InlineKeyboardMarkup().add(inline_btn)
    return inline_kb_accept

async def create_inline_order_collected(orderId):
    inline_btn = InlineKeyboardButton("Заказ собран", callback_data=orderId)
    inline_kb_order_collected = InlineKeyboardMarkup().add(inline_btn)
    return inline_kb_order_collected

async def create_inline_kb_date_delivery():
    today: datetime = datetime.date.today()
    keyboard = InlineKeyboardMarkup()
    for i in range(1, 4):
        delta = datetime.timedelta(hours=24)
        date = today + delta * i
        day = str(date.day) if date.day > 9 else '0' + str(date.day)
        keyboard.add(InlineKeyboardButton(str(date.month) + "." + day,
                                          callback_data=str(date.year) + '-' + str(date.month) + "-" + day))
    return keyboard

async def create_inline_kb_time_delivery(date):
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
    busyTime = set(api.getDeliveriesByDate(date))  # запрос занятых вермен для доставки
    freeTime = deliveryTime - busyTime  # вычитание множеств
    logger.info(f"create_inline_kb_time_delivery, busy times: {busyTime}")
    logger.info(f"create_inline_kb_time_delivery, free times: {freeTime}")
    deliveryTime = list(freeTime)
    deliveryTime.sort()
    for time in deliveryTime:
        keyboard.insert(InlineKeyboardButton(time, callback_data=time))
    return keyboard


def sortSizes(sizes: list):
    cmpSizes: dict = {"XS": 0, "S": 1, "M": 2, "L": 3, "XL": 4}
    sizes.sort(key=lambda x: cmpSizes[x])

async def create_inline_kb_sizes(type: str, capsule_size: str):
    # запрос доступных размеров одежды в капсулах определенного стиля и размера
    sizes = api.getSizesWithTypeSize(type, capsule_size)
    sizesM = []
    sizesW = []
    for size in sizes:
        if size.startswith('w'):
            sizesW.append(size[1:])
        elif size.startswith('m'):
            sizesM.append(size[1:])
        else:
            logger.error("incorrect size")
    cmpSizes: dict = {"XS": 0, "S": 1, "M": 2, "L": 3, "XL": 4}
    sizesM.sort(key=lambda x: cmpSizes[x])
    sizesW.sort(key=lambda x: cmpSizes[x])
    keyboard = InlineKeyboardMarkup(row_width=2)
    constSizes = ["XS", "S", "M", "L", "XL"]

    iterM = iter(sizesM)
    iterW = iter(sizesW)
    i = 0
    while i < len(constSizes):
        try:
            sizeW = next(iterW)
        except StopIteration:
            for index in range(i, len(constSizes)):
                sizesW.insert(index, "-")
        else:
            if sizeW != constSizes[i]:
                sizesW.insert(i, "-")
        try:
            sizeM = next(iterM)
        except StopIteration:
            for index in range(i, len(constSizes)):
                sizesM.insert(index, "-")
        else:
            if sizeM != constSizes[i]:
                sizesM.insert(i, "-")
        i += 1
    keyboard.row(InlineKeyboardButton("Мужские размеры", callback_data="мужские"),
                 InlineKeyboardButton("Женские размеры", callback_data="женские"))
    i = 0
    while i < len(constSizes):
        if sizesM[i] == sizesW[i] and sizesM[i] == '-':
            i += 1
            continue
        keyboard.row(InlineKeyboardButton(sizesM[i], callback_data="m" + sizesM[i]),
                     InlineKeyboardButton(sizesW[i], callback_data="w" + sizesW[i]))
        i += 1
    return keyboard
