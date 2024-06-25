import os

import aiohttp
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from aiogram.fsm.state import State, StatesGroup

import text
from routers.buy_module.buy_real_estate_kb import type_of_object_kb, calculation_format_buy_kb, mortgage_buy_kb, \
    type_of_object_detail_kb, type_of_object_detail_suburban_kb

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


@buy_real_estate_router.callback_query(F.data.contains("type_of_object_buy"))
@buy_real_estate_router.callback_query(F.data.contains("comm"))
@buy_real_estate_router.callback_query(F.data.contains("suburban"))
async def sell_real_estate_true(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split(',')
    if data[0] =='type_of_object_buy':
        await state.update_data(type_of_object_buy=callback_query.data.split(',')[1])
        await callback_query.message.delete()
        await callback_query.message.answer(
            f"Введите данные о вашем объекте в формате\n"
            f"предполагаемая стоимость,кол-во комнат,площадь,локация (район)\n"
            f"Пример: 1000000-4000000,2,60,Замоскворечье\n"
            f"Где 1000000-4000000 - предполагаемая стоимость(обязательно указывать диапазон,\n"
            f"2 - кол-во комнат, 60 - площадь, Замоскворечье - локация (район):",
        )
    elif data[0] == 'comm' and data[1] != 'Земельный участок':
        await state.update_data(type_of_object_buy_detail=callback_query.data.split(',')[1])
        await callback_query.message.delete()
        await callback_query.message.answer(
            f"Введите данные о вашем объекте в формате\n"
            f"предполагаемая стоимость,площадь,локация (район, тракт, населенный пункт)\n"
            f"Пример: 1000000-4000000,60-120,Замоскворечье\n"
            f"Где 1000000-4000000 - предполагаемая стоимость(обязательно указывать диапазон),\n"
            f"60-120 - площадь(обязателен диапазон), Замоскворечье - локация (район, тракт, населенный пункт):",
        )
    elif data[0] == 'comm' and data[1] == 'Земельный участок':
        await state.update_data(type_of_object_buy_detail=callback_query.data.split(',')[1])
        await callback_query.message.delete()
        await callback_query.message.answer(
            f"Введите данные о вашем объекте в формате\n"
            f"предполагаемая стоимость,площадь,локация (район, тракт, населенный пункт)\n"
            f"Пример: 1000000-4000000,60-120,Замоскворечье\n"
            f"Где 1000000-4000000 - предполагаемая стоимость(обязательно указывать диапазон),\n"
            f"60-120 - площадь(обязателен диапазон), Замоскворечье - локация (район, тракт, населенный пункт):",
        )
    elif data[0] == 'suburban' and data[1] != 'Земельный участок':
        await state.update_data(type_of_object_buy_detail=callback_query.data.split(',')[1])
        await callback_query.message.delete()
        await callback_query.message.answer(
            f"Введите данные о вашем объекте в формате\n"
            f"предполагаемая стоимость,количество комнат,площадь дома,\n"
            f"площадь земельного участка(0т-до),локация (район, тракт, населенный пункт)\n"
            f"Пример: 1000000-4000000,5,120,1000-2000,Замоскворечье\n"
            f"Где 1000000-4000000 - предполагаемая стоимость(обязательно указывать диапазон),\n"
            f"5 - количество комнат, 120 - площадь дома, 1000-2000 - площадь земельного участка(обязателен диапазон),\n"
            f"Замоскворечье - локация (район, тракт, населенный пункт):",
        )
    else:
        await state.update_data(type_of_object_buy_detail=callback_query.data.split(',')[1])
        await callback_query.message.delete()
        await callback_query.message.answer(
            f"Введите данные о вашем объекте в формате\n"
            f"предполагаемая стоимость,площадь,локация (район, тракт, населенный пункт)\n"
            f"Пример: 1000000-4000000,60-120,Замоскворечье\n"
            f"Где 1000000-4000000 - предполагаемая стоимость(обязательно указывать диапазон),\n"
            f"60-120 - площадь(обязателен диапазон), Замоскворечье - локация (район, тракт, населенный пункт):",
        )


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


# @router.callback_query(F.data.contains("type_of_object"))
# async def type_of_object(callback_query: CallbackQuery, state: FSMContext):
#     await state.set_state(SellPattern.TYPE_OF_OBJECT)
#     await state.update_data(TYPE_OF_OBJECT=callback_query.data.split(',')[1])
#     # await state.set_state(UserData.GENDER.state.split(',')[0])
#     await callback_query.message.delete()
#     user_data = await state.get_data()
#     print(user_data)
#     if user_data['IS_TRUE'] == "True":
#         await callback_query.message.answer(
#             f"Введите данные о вашем объекте в формате\n"
#             f"Адрес недвижимости,Площадь объекта,кол-во комнат\n"
#             f"Пример: г. Москва ул. Автомоторная д 5 кв 13,54,3\n"
#             f"Где г. Москва ул. Автомоторная д 5 кв 13 - адрес, "
#             f"54 - площадь объекта в кв метрах, 3 - количество комнат: "
#         )
#     else:
#         await callback_query.message.answer(
#             f"Введите данные о вашем объекте в формате\n"
#             f"Адрес недвижимости - адрес\n"
#             f"Пример: Адрес недвижимости - г. Москва ул. Автомоторная д 5 кв 13"
#         )


@buy_real_estate_router.message(F.text.regexp(r'.*?,.*?,.*?,.*'))
@buy_real_estate_router.message(F.text.regexp(r'.*?,.*?,.*?,.*?,.*'))
@buy_real_estate_router.message(F.text.regexp(r'^(\d+)-(\d+),(\d+)-(\d+),(.+)$'))
async def type_of_object(message: types.Message, state: FSMContext):
    print(message.text)
    data = message.text.split(',')
    if len(data) == 4:
        await state.update_data(price=data[0])
        await state.update_data(number_of_rooms=data[1])
        await state.update_data(square=data[2])
        await state.update_data(location=data[3])
    elif len(data) == 3:
        await state.update_data(price=data[0])
        await state.update_data(square=data[1])
        await state.update_data(location=data[2])
    else:
        await state.update_data(price=data[0])
        await state.update_data(number_of_rooms=data[1])
        await state.update_data(square_house=data[2])
        await state.update_data(land_plot_square=data[3])
        await state.update_data(location=data[4])
    user_data = await state.get_data()
    print(user_data.items())

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
    await callback_query.message.answer(
        f"В ближайшее время Вам будет направлена подборка\n"
        f"объектов недвижимости. Если у Вас возникнут вопросы\n"
        f"или потребуются изменения выбранных условий вы можете\n"
        f"обратиться в чат."
        f"Ваши данные: {user_data.items()}"
        f"\nсделать пересылку данных юзера риелтору"
    )
