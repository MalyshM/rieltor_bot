from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

type_of_object_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Вторичная", callback_data="type_of_object_buy,Вторичная"),
     InlineKeyboardButton(text="Новостройка(бесплатно)", callback_data="type_of_object_buy,Новостройка(бесплатно)")],
    [InlineKeyboardButton(text="Загородная", callback_data="type_of_object_detail_buy,Загородная"),
     InlineKeyboardButton(text="Коммерческая", callback_data="type_of_object_detail_buy,Коммерческая")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])
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
    [InlineKeyboardButton(text="Земельный участок",
                          callback_data="suburban,Земельный участок")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])
calculation_format_buy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ипотека", callback_data="mortgage,Ипотека"),
     InlineKeyboardButton(text="Собственные средства", callback_data="calculation_format_buy_kb,Собственныесредства")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])
mortgage_buy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Уже имеется одобрение", callback_data="calculation_format_buy_kb,True"),
     InlineKeyboardButton(text="Ипотека требует одобрения", callback_data="mortgage_true")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])
