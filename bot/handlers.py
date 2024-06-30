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


@router.callback_query(F.data == "Request_a_consultation_by_phone")
async def menu(msg: Message):
    await msg.message.delete()
    await msg.message.answer("сделать пересылку данных юзера риелтору")


class Question(StatesGroup):
    question = State()


@router.message(Question.question)
async def menu(msg: Message, state: FSMContext):
    # await msg.delete()
    await msg.answer("сделать пересылку данных юзера и вопроса риелтору"
                     f'\nВаш вопрос: {msg.text}')


@router.callback_query(F.data == "Ask_your_question")
async def menu(msg: Message, state: FSMContext):
    await msg.message.delete()
    await state.set_state(Question.question)
    await msg.message.answer("Введите свой вопрос:")


@router.callback_query(F.data == "deals_of_the_week")
async def deals_of_the_week(msg: Message, state: FSMContext):
    await msg.message.delete()
    await msg.message.answer(
        f"Выберите интересующую вас категорию: ",
        reply_markup=kb.Get_the_best_deals_of_the_week_kb_1
    )


@router.callback_query(F.data.contains("best_deals_of_the_week"))
async def deals_of_the_week(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    data = callback_query.data.split(',')
    if data[1] == '1':
        await callback_query.message.answer(
            f"*высылать ссылку на подборку*: "
        )
    elif data[1] == '2':
        await callback_query.message.answer(
            f"*высылать ссылку на подборку*: "
        )
    else:
        await callback_query.message.answer(
            f"Выберите интересующую вас категорию: ",
            reply_markup=kb.Get_the_best_deals_of_the_week_kb_2
        )


@router.callback_query(F.data.contains("best_new_building_deals_of_the_week"))
async def deals_of_the_week(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    data = callback_query.data.split(',')
    if data[1] == '1':
        await callback_query.message.answer(
            f"*высылать ссылку на подборку*: "
        )
    elif data[1] == '2':
        await callback_query.message.answer(
            f"*высылать ссылку на подборку*: "
        )
    else:
        await callback_query.message.answer(
            f"*высылать ссылку на подборку*: "
        )


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
    await state.set_state(SellPattern.ADDRESS)
    await callback_query.message.answer('Введите адрес объекта. Пример:\nг. Москва ул. Автомоторная д 5 кв 13')


@router.message(SellPattern.ADDRESS)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    user_data = await state.get_data()
    if user_data['IS_TRUE'] != "True":
        await type_of_object_final(message, state)
    else:
        await state.set_state(SellPattern.SQUARE)
        # await message.delete()
        await message.answer("Введите площадь объекта в квадратных метрах. Пример:\n50")


@router.message(SellPattern.SQUARE)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(square=message.text)
    await state.set_state(SellPattern.NUMBER_OF_ROOMS)
    # await message.delete()
    await message.answer("Введите количество комнат. Пример:\n3")


@router.message(SellPattern.NUMBER_OF_ROOMS)
async def type_of_object_final(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['IS_TRUE'] == "True":
        await state.update_data(number_of_rooms=message.text)
    user_data = await state.get_data()
    await state.clear()
    await message.answer(
        f"В ближайшее время Вам будет направлена примерная стоимость вашей недвижимости\n"
        f"Ваши данные: {user_data.items()}"
        f"\nсделать пересылку данных юзера риелтору"
    )

# @router.message()
# async def unhandled_message(message: types.Message):
#     print(message.text)
#     await message.answer("Извините, я не могу обработать этот запрос. Пожалуйста, попробуйте что-нибудь другое.")
