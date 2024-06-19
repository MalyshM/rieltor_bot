import os

import aiohttp
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
import kb
import text
from aiogram.fsm.state import State, StatesGroup

from user_funcs import add_user

# from requests import add_user, check_resp

router = Router()


class SellPattern(StatesGroup):
    IS_TRUE = State()
    TYPE_OF_OBJECT = State()
    ADDRESS = State()
    SQUARE = State()
    NUMBER_OF_ROOMS = State()


class UserData(StatesGroup):
    NAME = State()
    GENDER = State()
    YEAR = State()
    MONTH = State()
    DAY = State()
    HHMM = State()
    PLACE = State()


@router.message(Command("start"))
async def start_handler(msg: Message):
    try:
        resp = await add_user(msg.from_user.id)
        if isinstance(resp, str):
            raise resp
    except Exception as e:
        print(e)
        pass
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
@router.callback_query(F.data == "menu")
@router.callback_query(F.data == "restart")
async def menu(msg: Message):
    await msg.message.delete()
    await msg.message.answer(text.menu, reply_markup=kb.menu)


# default way of displaying a selector to user - date set for today
@router.callback_query(F.data == "sell_real_estate")
async def sell_real_estate(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserData.NAME)

    await state.update_data(name=callback_query.from_user.full_name)
    await state.update_data(id=callback_query.from_user.id)
    await state.update_data(url=callback_query.from_user.url)
    try:
        await state.update_data(username='@' + callback_query.from_user.username)
    except:
        await state.update_data(username='No username')
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Вы хотите указать только тип объекта либо же получить дополнительно приблизительную стоимость вашего объекта?: ",
        reply_markup=kb.sell_real_estate
    )


@router.callback_query(F.data.contains("sell_real_estate_true"))
async def sell_real_estate_true(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(SellPattern.IS_TRUE)
    await state.update_data(IS_TRUE=callback_query.data.split(',')[1])
    await callback_query.message.delete()
    user_data = await state.get_data()
    print(user_data)
    data = callback_query.data.split(',')
    print(data)
    await callback_query.message.answer(
        f"Выберите тип объекта: ",
        reply_markup=kb.type_of_object
    )


@router.callback_query(F.data.contains("type_of_object_sell"))
async def type_of_object(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(SellPattern.TYPE_OF_OBJECT)
    data = callback_query.data.split(',')[1]
    if data == 'Комм':
        await state.update_data(TYPE_OF_OBJECT='Коммерческая недвижимость')
    else:
        await state.update_data(TYPE_OF_OBJECT=data)
    # await state.set_state(UserData.GENDER.state.split(',')[0])
    await callback_query.message.delete()
    user_data = await state.get_data()
    print(user_data)
    if user_data['IS_TRUE'] == "True":
        await callback_query.message.answer(
            f"Введите данные о вашем объекте в формате\n"
            f"Адрес недвижимости,Площадь объекта,кол-во комнат\n"
            f"Пример: г. Москва ул. Автомоторная д 5 кв 13,54,3\n"
            f"Где г. Москва ул. Автомоторная д 5 кв 13 - адрес, "
            f"54 - площадь объекта в кв метрах, 3 - количество комнат: "
        )
    else:
        await callback_query.message.answer(
            f"Введите данные о вашем объекте в формате\n"
            f"Адрес недвижимости - адрес\n"
            f"Пример: Адрес недвижимости - г. Москва ул. Автомоторная д 5 кв 13"
        )


@router.message(F.text.regexp(r'^.*?,\d+,\d+$'))
@router.message(F.text.regexp(r'Адрес недвижимости - '))
async def type_of_object(message: types.Message, state: FSMContext):
    await state.set_state(SellPattern.ADDRESS)
    await state.set_state(SellPattern.SQUARE)
    await state.set_state(SellPattern.NUMBER_OF_ROOMS)
    if 'Адрес недвижимости - ' in message.text:
        data = message.text.replace('Адрес недвижимости - ', '')
        await state.update_data(ADDRESS=data)
    else:
        data = message.text.split(',')
        await state.update_data(ADDRESS=data[0])
        await state.update_data(SQUARE=data[1])
        await state.update_data(NUMBER_OF_ROOMS=data[2])
    user_data = await state.get_data()
    await state.clear()
    await message.answer(
        f"В ближайшее время Вам будет направлена примерная стоимость вашей недвижимости\n"
        f"Ваши данные: {user_data.items()}"
    )


# @router.message()
# async def unhandled_message(message: types.Message):
#     print(message.text)
#     await message.answer("Извините, я не могу обработать этот запрос. Пожалуйста, попробуйте что-нибудь другое.")
