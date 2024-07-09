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
    [InlineKeyboardButton(text="Получить лучшие предложения за неделю", callback_data="deals_of_the_week")],
]

admin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить/обновить подборку", callback_data="object_deals")],
    [InlineKeyboardButton(text="Ваши подборки", callback_data="get_object_deals")],
    [InlineKeyboardButton(text="Узнать историю заявок пользователя(в разработке)", callback_data="aaa")],
    [InlineKeyboardButton(text="Узнать количество подписчиков(в разработке)",
                          callback_data="aaa")],
])

type_of_object_deals_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Загородная", callback_data="type_of_object_deals,Загородная"),
     InlineKeyboardButton(text="Вторичка", callback_data="type_of_object_deals,Вторичка")],
    [InlineKeyboardButton(text="Нов. без ПВ", callback_data="type_of_object_deals,Нов. без ПВ"),
     InlineKeyboardButton(text="Самые дешевые", callback_data="type_of_object_deals,Самые дешевые")],
    [InlineKeyboardButton(text="Акции и траншевая ипотека",
                          callback_data="type_of_object_deals,Акц")],
])

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

sell_real_estate = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Указать тип объекта", callback_data="sell_real_estate_true,False")],
    [InlineKeyboardButton(text="Получить дополнительно приблизительную стоимость вашего объекта",
                          callback_data="sell_real_estate_true,True")]
])
type_of_user_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пользователь", callback_data="menu")],
    [InlineKeyboardButton(text="Риелтор", callback_data="admin")]
])
type_of_object = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Квартира", callback_data="type_of_object_sell,Квартира"),
     InlineKeyboardButton(text="Строится", callback_data="type_of_object_sell,Строится")],
    [InlineKeyboardButton(text="Земельный участок", callback_data="type_of_object_sell,Земельный_участок"),
     InlineKeyboardButton(text="Загородный дом", callback_data="type_of_object_sell,Загородный_дом")],
    [InlineKeyboardButton(text="Коммерческая недвижимость", callback_data="type_of_object_sell,Комм")],
])

Get_the_best_deals_of_the_week_kb_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Загородная", callback_data="best_deals_of_the_week,1")],
    [InlineKeyboardButton(text="Вторичка", callback_data="best_deals_of_the_week,2")],
    [InlineKeyboardButton(text="Новостройка", callback_data="best_deals_of_the_week,3")],
])

Get_the_best_deals_of_the_week_kb_2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Нов. без ПВ", callback_data="best_new_building_deals_of_the_week,1")],
    [InlineKeyboardButton(text="Самые дешевые", callback_data="best_new_building_deals_of_the_week,2")],
    [InlineKeyboardButton(text="Акции и траншевая ипотека", callback_data="best_new_building_deals_of_the_week,3")],
])
