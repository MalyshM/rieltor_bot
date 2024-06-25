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


class MortgageApplication(StatesGroup):
    full_name = State()
    birth_date = State()
    phone = State()
    monthly_income = State()
    workplace = State()
    work_phone = State()
    credit_amount = State()


# default way of displaying a selector to user - date set for today
@mortgage_router.callback_query(F.data == "mortgage_true")
async def mortgage_init(callback_query: CallbackQuery, state: FSMContext):
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
    if len(data) > 1:
        await state.update_data(family_mortgage=data[1])
        await state.update_data(rural_mortgage=data[2])
        await state.update_data(base_rate=data[3])
        await state.update_data(IT_mortgage=data[4])
        await state.update_data(state_support_2020=data[5])
    await callback_query.message.delete()
    await state.set_state(MortgageApplication.full_name)
    await callback_query.message.answer("Введите Ваше ФИО:")


@mortgage_router.message(MortgageApplication.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(MortgageApplication.birth_date)
    # await message.delete()
    await message.answer("Введите Вашу дату рождения (DD.MM.YYYY):")


@mortgage_router.message(MortgageApplication.birth_date)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await state.set_state(MortgageApplication.phone)
    # await message.delete()
    await message.answer("Введите Ваш номер телефона:")


@mortgage_router.message(MortgageApplication.phone)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(MortgageApplication.monthly_income)
    # await message.delete()
    await message.answer("Введите Вашу зп в месяц:")


@mortgage_router.message(MortgageApplication.monthly_income)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(monthly_income=message.text)
    await state.set_state(MortgageApplication.workplace)
    # await message.delete()
    await message.answer("Введите Ваше место работы:")


@mortgage_router.message(MortgageApplication.workplace)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(workplace=message.text)
    await state.set_state(MortgageApplication.work_phone)
    # await message.delete()
    await message.answer("Введите Ваш рабочий телефон:")


@mortgage_router.message(MortgageApplication.work_phone)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(work_phone=message.text)
    await state.set_state(MortgageApplication.credit_amount)
    # await message.delete()
    await message.answer("Введите Ваше необходимое количество кредитных средств:")


# Аналогичные обработчики для остальных полей

@mortgage_router.message(MortgageApplication.credit_amount)
async def get_credit_amount(message: types.Message, state: FSMContext):
    await state.update_data(credit_amount=message.text)
    # await message.delete()
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "В скором времени будет сформирована заявка в банк и в случае "
        "необходимости уточнения информация с Вами свяжется ипотечный "
        "специалист." f'\n Ваши данные: {data}'
        f"\nсделать пересылку данных юзера риелтору"
    )
