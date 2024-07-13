import os

import aiohttp
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from aiogram.fsm.state import State, StatesGroup

import text
from admin_crud import get_admin
from models import connect_db
from routers.buy_module.buy_real_estate_kb import type_of_object_kb, calculation_format_buy_kb, mortgage_buy_kb, \
    type_of_object_detail_kb, type_of_object_detail_suburban_kb
from send_mail import send_email
from user_funcs import get_user

# from requests import add_user, check_resp

buy_real_estate_router = Router()


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
@buy_real_estate_router.callback_query(F.data == "buy_real_estate")
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
        "Укажите тип объекта: ",
        reply_markup=type_of_object_kb
    )


class BuyPattern(StatesGroup):
    cost_range = State()
    number_of_rooms = State()
    square = State()
    house_square = State()
    land_square = State()
    location = State()


@buy_real_estate_router.callback_query(F.data.contains("type_of_object_buy"))
@buy_real_estate_router.callback_query(F.data.contains("comm"))
@buy_real_estate_router.callback_query(F.data.contains("suburban"))
async def sell_real_estate_true(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split(',')
    if data[0] == 'type_of_object_buy':
        await state.update_data(type_of_object_buy=callback_query.data.split(',')[1])
    else:
        await state.update_data(type_of_object_buy_detail=callback_query.data.split(',')[1])
    await callback_query.message.delete()
    await state.set_state(BuyPattern.cost_range)
    await callback_query.message.answer('Введите предполагаемую вилку стоимости.\nПример: 1000000-3000000')


@buy_real_estate_router.callback_query(F.data.contains("type_of_object_detail_buy"))
async def sell_real_estate_true(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split(',')
    if data[1] == 'Коммерческая':
        await state.update_data(type_of_object_buy=callback_query.data.split(',')[1])
        await callback_query.message.delete()
        await callback_query.message.answer(
            f"Введите тип вашего коммерческого объекта:",
            reply_markup=type_of_object_detail_kb
        )
    else:
        await state.update_data(type_of_object_buy=callback_query.data.split(',')[1])
        await callback_query.message.delete()
        await callback_query.message.answer(
            f"Введите тип вашего загородного объекта:",
            reply_markup=type_of_object_detail_suburban_kb
        )


@buy_real_estate_router.message(BuyPattern.cost_range)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(cost_range=message.text)
    user_data = await state.get_data()
    if 'type_of_object_buy_detail' in user_data.keys():
        print(user_data)
        print(user_data.values())
        if 'Загородная' in user_data.values() or 'Земельный участок' in user_data.values():
            await state.set_state(BuyPattern.land_square)
            await message.answer("Введите вилку площади желаемого участка в квадратных метрах. Пример:\n1000-2000")
        else:
            await state.set_state(BuyPattern.square)
            await message.answer("Введите вилку площади желаемого объекта в квадратных метрах. Пример:\n1000-2000")
    else:
        await state.set_state(BuyPattern.number_of_rooms)
        await message.answer("Введите количество комнат. Пример:\n5")

    # await message.delete()


@buy_real_estate_router.message(BuyPattern.land_square)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(land_square=message.text)
    user_data = await state.get_data()
    if 'Земельный участок' in user_data.values():
        await state.set_state(BuyPattern.location)
        await message.answer("Введите желаемый район/тракт/населенный пункт. Пример:\nТюмень район Обороны")
    else:
        await state.set_state(BuyPattern.number_of_rooms)
        await message.answer("Введите количество комнат. Пример:\n5")


@buy_real_estate_router.message(BuyPattern.number_of_rooms)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(number_of_rooms=message.text)
    user_data = await state.get_data()
    await state.set_state(BuyPattern.square)
    if 'type_of_object_buy_detail' in user_data.keys():
        await message.answer("Введите площадь дома. Пример:\n200")
    else:
        await message.answer("Введите площадь квартиры. Пример:\n50")


@buy_real_estate_router.message(BuyPattern.square)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(square=message.text)
    await state.set_state(BuyPattern.location)
    await message.answer("Введите желаемый район/тракт/населенный пункт. Пример:\nТюмень район Обороны")


@buy_real_estate_router.message(BuyPattern.location)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer(
        f"Формат расчета: \n",
        reply_markup=calculation_format_buy_kb
    )


@buy_real_estate_router.callback_query(F.data.contains("mortgage"))
async def mortgage(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split(',')
    await state.update_data(calculation_format=data[1])
    await callback_query.message.delete()
    await callback_query.message.answer(
        f"Статус ипотеки: ",
        reply_markup=mortgage_buy_kb
    )


@buy_real_estate_router.callback_query(F.data.contains("calculation_format_buy_kb"))
async def calculation_format_buy(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split(',')
    if data[1] == 'Собственныесредства':
        await state.update_data(calculation_format='Собственные средства')
    else:
        await state.update_data(is_approved=data[1])
    user_data = await state.get_data()
    await state.clear()
    await callback_query.message.delete()
    async with connect_db() as session:
        user = await get_user(session, user_data['id'])
        admin = await get_admin(session, user.admin_id)
    res = send_email(to_email=admin.email, subject='Пришла заявка на покупку',
                     message=f'Данные пользователя: {user_data.items()}')
    await callback_query.message.answer(
        f"В ближайшее время Вам будет направлена подборка\n"
        f"объектов недвижимости. Если у Вас возникнут вопросы\n"
        f"или потребуются изменения выбранных условий вы можете\n"
        f"обратиться в чат."
    )
