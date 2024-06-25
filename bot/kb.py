from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
import calendar
import urllib.parse

menu = [
    [InlineKeyboardButton(text="Я хочу продать недвижимость", callback_data="sell_real_estate")],
     [InlineKeyboardButton(text="Я хочу купить недвижимость", callback_data="buy_real_estate")],
    [InlineKeyboardButton(text="Ипотека(все операции бесплатно)", callback_data="mortgage_true")],
     [InlineKeyboardButton(text="Запросить консультацию по телефону", callback_data="Request_a_consultation_by_phone")],
    [InlineKeyboardButton(text="Задать свой вопрос", callback_data="Ask_your_question")],
     [InlineKeyboardButton(text="Получить лучшие предложения за неделю", callback_data="sell_real_estate")],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

sell_real_estate = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Указать тип объекта", callback_data="sell_real_estate_true,False")],
        [InlineKeyboardButton(text="Получить дополнительно приблизительную стоимость вашего объекта",
                             callback_data="sell_real_estate_true,True")
    ]
])

type_of_object = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Квартира", callback_data="type_of_object_sell,Квартира"),
     InlineKeyboardButton(text="Строится", callback_data="type_of_object_sell,Строится")],
    [InlineKeyboardButton(text="Земельный участок", callback_data="type_of_object_sell,Земельный_участок"),
     InlineKeyboardButton(text="Загородный дом", callback_data="type_of_object_sell,Загородный_дом")],
    [InlineKeyboardButton(text="Коммерческая недвижимость", callback_data="type_of_object_sell,Комм")],
])