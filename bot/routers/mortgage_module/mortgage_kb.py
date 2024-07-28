from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

mortgage_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Получить информацию по ипотечным программам", callback_data="years")],
    [InlineKeyboardButton(text="Подать заявку на ипотеку", callback_data="make_mortgage")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])
number_of_children_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="2 и более", callback_data="18_or_older,2 и более")],
    [InlineKeyboardButton(text="1 ребенок", callback_data="is_2018_+,1 ребенок")],
    [InlineKeyboardButton(text="Нет", callback_data="make_mortgage,0,1,1,1,1")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])

is_2018_ = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="make_mortgage,0,1,1,1,1")],
    [InlineKeyboardButton(text="Нет", callback_data="make_mortgage,1,1,0,0,1")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])

is_18_or_older = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="make_mortgage,0,1,1,1,1")],
    [InlineKeyboardButton(text="Нет", callback_data="make_mortgage,1,1,0,0,1")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])


async def get_year_calendar(offset: int = 0) -> InlineKeyboardMarkup:
    start_year = 20 + offset
    builder = InlineKeyboardBuilder()

    for i in range(15):
        builder.button(text=f"{start_year}", callback_data=f"{start_year},number_of_children")
        start_year += 1
    builder.button(text=f"Назад", callback_data=f"{offset},year_of_birth,back")
    builder.button(text=f"В меню", callback_data=f"menu")
    builder.button(text=f"Вперед", callback_data=f"{offset},year_of_birth,forward")
    builder.adjust(3)
    keyboard_markup = builder.as_markup()
    return keyboard_markup


type_of_object_detail_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Земельный участок", callback_data="comm,Земельный участок"),
     InlineKeyboardButton(text="Торговое помещение", callback_data="comm,Торговое помещение")],
    [InlineKeyboardButton(text="Склад", callback_data="comm,Склад"),
     InlineKeyboardButton(text="Производственное", callback_data="comm,Производственное")],
    [InlineKeyboardButton(text="Офисное", callback_data="comm,Офисное"),
     InlineKeyboardButton(text="Свой вариант", callback_data="comm,Свой вариант")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])
type_of_object_detail_suburban_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Готовый дом", callback_data="suburban,Готовый дом"),
     InlineKeyboardButton(text="Подряд на стройку", callback_data="suburban,Подряд на стройку")],
    [InlineKeyboardButton(text="Земельный участок", callback_data="suburban,Земельный участок")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])
calculation_format_buy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ипотека", callback_data="mortgage,Ипотека"),
     InlineKeyboardButton(text="Собственные средства", callback_data="calculation_format_buy_kb,Собственныесредства")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])

mortgage_buy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Уже имеется одобрение", callback_data="calculation_format_buy_kb,True"),
     InlineKeyboardButton(text="Ипотека требует одобрения", callback_data="asd")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])
