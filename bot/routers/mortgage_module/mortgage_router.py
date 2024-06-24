import os

import aiohttp
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from aiogram.fsm.state import State, StatesGroup

import text
from routers.mortgage_module.mortgage_kb import mortgage_info, get_year_calendar, number_of_children_kb, is_2018_, \
    is_18_or_older

# from requests import add_user, check_resp

mortgage_router = Router()


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


# default way of displaying a selector to user - date set for today
@mortgage_router.callback_query(F.data == "mortgage_true")
async def mortgage_init(callback_query: CallbackQuery, state: FSMContext):
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
        "Укажите желаемое действие: ",
        reply_markup=mortgage_info
    )


@mortgage_router.callback_query(F.data == "years")
@mortgage_router.callback_query(F.data.contains("year_of_birth"))
async def year(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    user_data = await state.get_data()

    data = callback_query.data.split(',')
    print(data)
    if len(data) == 3:
        if data[2] == "back":
            await callback_query.message.answer(
                f"Сколько вам лет?",
                reply_markup=await get_year_calendar(int(data[0]) - 15)
            )
        elif data[2] == "forward":
            await callback_query.message.answer(
                f"Сколько вам лет?",
                reply_markup=await get_year_calendar(int(data[0]) + 15)
            )
    else:
        await state.update_data(gender=callback_query.data.split(',')[0])
        user_data = await state.get_data()
        print(user_data)
        await callback_query.message.answer(
            f"Сколько вам лет?",
            reply_markup=await get_year_calendar()
        )


@mortgage_router.callback_query(F.data.contains("number_of_children"))
async def sell_real_estate_true(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split(',')
    await state.update_data(years=data[0])
    await callback_query.message.delete()
    await callback_query.message.answer(
        f"Сколько у вас детей?",
        reply_markup=number_of_children_kb
    )


@mortgage_router.callback_query(F.data.contains("is_2018_+"))
async def sell_real_estate_true(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split(',')
    await state.update_data(children=data[1])
    await callback_query.message.delete()
    await callback_query.message.answer(
        f"Рождены после 1 января 2018 года?",
        reply_markup=is_2018_
    )


@mortgage_router.callback_query(F.data.contains("18_or_older"))
async def sell_real_estate_true(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split(',')
    await state.update_data(children=data[1])
    await callback_query.message.delete()
    await callback_query.message.answer(
        f"Дети старше 18 лет?",
        reply_markup=is_18_or_older
    )


@mortgage_router.callback_query(F.data.contains("make_mortgage"))
async def sell_real_estate_true(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split(',')
    await state.update_data(family_mortgage=data[1])
    await state.update_data(rural_mortgage=data[2])
    await state.update_data(base_rate=data[3])
    await state.update_data(IT_mortgage=data[4])
    await state.update_data(state_support_2020=data[5])
    await callback_query.message.delete()
    user_data = await state.get_data()
    await state.clear()
    await callback_query.message.answer(
        '''1.ФИО 2. Дата рождения 3. Телефон 4. Ежемесячный доход 5. Место работы 6. Рабочий телефон 7. необходимая сумма кредитных средств.'''
        f"Дети старше 18 лет?"
        f"Ваши данные: {user_data.items()}",
        reply_markup=is_18_or_older
    )
