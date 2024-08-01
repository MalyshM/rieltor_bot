from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
user_fields = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Я хочу заполнить все поля",
                          callback_data="fffff")],
    [InlineKeyboardButton(text="Заполнить номер телефона",
                          callback_data="fffff")],
    [InlineKeyboardButton(
        text="Заполнить шаблон для получения вариантов ипотеки", callback_data="mortgage_true")],
    [InlineKeyboardButton(text="Заполнить шаблон для оформления ипотеки",
                          callback_data="fffff")],
    [InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")],
])
