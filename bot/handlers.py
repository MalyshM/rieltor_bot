import os
import re

import aiohttp
from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
import kb
import text
from aiogram.fsm.state import State, StatesGroup

from admin_crud import get_admin, update_admin, get_admin_users
from key_dict import prettify_dict_str
from models import connect_db
from selection_crud import create_selection, update_selection, get_all_selections, get_all_selections_by_admin
from send_mail import send_email
from user_funcs import create_user, get_user, update_user

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
    admin_id = State()
    email = State()
    deal_link = State()
    phone_number = State()


@router.message(Command('start'))
async def start_handler(msg: Message, command: CommandObject):
    args = command.args
    print(args)
    if args:
        try:
            data = {'name': msg.from_user.full_name, 'id': msg.from_user.id, 'url': msg.from_user.url}
            try:
                data['username'] = '@' + msg.from_user.username
            except:
                data['username'] = 'No username'
            data['admin_id'] = int(args)
            async with connect_db() as session:
                resp = await create_user(session, data)
            if isinstance(resp, str):
                raise resp
        except Exception as e:
            print(e)
            pass
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.type_of_user_kb)


@router.message(Command("menu"))
@router.callback_query(F.data == "menu")
@router.callback_query(F.data == "back_to_menu")
@router.message(UserData.admin_id)
async def menu(msg: Message, state: FSMContext):
    await state.clear()
    try:
        if isinstance(int(msg.text), int):
            print(msg.text)
            async with connect_db() as session:
                res = await update_user(session, msg.from_user.id, admin_id=int(msg.text))
                print(res.tg_id)
                print(res.admin_id)
    except:
        pass
    try:
        data = {'name': msg.from_user.full_name, 'id': msg.from_user.id, 'url': msg.from_user.url}
        try:
            data['username'] = '@' + msg.from_user.username
        except:
            data['username'] = 'No username'
        async with connect_db() as session:
            resp = await create_user(session, data)
        if isinstance(resp, str):
            raise resp
    except Exception as e:
        print(e)
        pass
    async with connect_db() as session:
        resp = await get_user(session, msg.from_user.id)
        print(resp.tg_id)
        print(resp.admin_id)
        if resp.admin_id == 981942668:
            await state.set_state(UserData.admin_id)
            try:
                await msg.message.delete()
                await msg.message.answer("Введите код вашего риелтора для просмотра")
            except:
                await msg.delete()
                await msg.answer("Введите код вашего риелтора для просмотра")
        else:
            await state.update_data(name=msg.from_user.full_name)
            await state.update_data(id=msg.from_user.id)
            await state.update_data(url=msg.from_user.url)
            try:
                await state.update_data(username='@' + msg.from_user.username)
            except:
                await state.update_data(username='No username')
            try:
                await msg.message.answer("Выберите интересующий вас раздел", reply_markup=kb.menu)
            except:
                await msg.answer("Выберите интересующий вас раздел", reply_markup=kb.menu)


@router.callback_query(F.data == "another_rieltor_code")
@router.message(UserData.admin_id)
async def another_rieltor_code(message: Message, state: FSMContext):
    try:
        print(isinstance(int(message.text), int))
        if isinstance(int(message.text), int):
            print(message.text)
            async with connect_db() as session:
                res = await update_user(session, message.from_user.id, admin_id=int(message.text))
                print(res.tg_id)
                print(res.admin_id)
    except:
        pass
    await state.set_state(UserData.admin_id)
    # await message.delete()
    await message.message.answer("Введите Ваш новый код риелтора:", reply_markup=kb.exit_to_menu_kb)


@router.message(Command("admin"))
@router.callback_query(F.data == "admin")
@router.message(UserData.email)
async def admin(msg: Message, state: FSMContext):
    await state.update_data(tg_id=msg.from_user.id)
    try:
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', msg.text):
            print(msg.text)
            async with connect_db() as session:
                res = await update_admin(session, msg.from_user.id, email=msg.text)
    except:
        pass
    try:
        async with connect_db() as session:
            resp = await get_admin(session, msg.from_user.id)
            # print(resp.email)
            if resp is None:
                await msg.message.answer("Вам запрещен вход в этот отдел", reply_markup=kb.menu)
            if resp.email == 'asd':
                await state.set_state(UserData.email)
                await msg.message.answer("Введите свою почту для дальнейшего получения заявок от пользователей")
            else:
                try:
                    await msg.message.answer("Выберите интересующий вас раздел", reply_markup=kb.admin_kb)
                except:
                    await msg.answer("Выберите интересующий вас раздел", reply_markup=kb.admin_kb)
        if isinstance(resp, str):
            raise resp
    except Exception as e:
        print(e)
        pass


@router.callback_query(F.data == "get_admin_users")
async def get_admin_users_route(callback_query: CallbackQuery, state: FSMContext):
    admin_data = await state.get_data()
    async with connect_db() as session:
        resp = await get_admin_users(session, admin_data['tg_id'])
        print(resp)
    await callback_query.message.answer(f"Пользователи, подписанные на вас: {resp}")


@router.callback_query(F.data == "object_deals")
async def object_deals(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Выберите интересующую вас подборку", reply_markup=kb.type_of_object_deals_kb)


@router.callback_query(F.data == "get_object_deals")
async def object_deals(callback_query: CallbackQuery, state: FSMContext):
    async with connect_db() as session:
        data = await state.get_data()
        res = await get_all_selections_by_admin(session, data['tg_id'])
        result_str = ''
        for row in res:
            result_str += f'Тип - {row["type_of"]}, Ссылка - {row["link"]}\n'
    await callback_query.message.answer(f'Ваши подборки:\n{result_str}')
    await callback_query.message.answer("Выберите интересующий вас раздел", reply_markup=kb.admin_kb)


@router.callback_query(F.data.contains("type_of_object_deals"))
async def deals_of_the_week(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(type_of=callback_query.data.split(',')[1])
    await state.set_state(UserData.deal_link)
    await callback_query.message.answer("Введите ссылку на подборку:")


@router.message(UserData.deal_link)
async def add_deal_link(msg: Message, state: FSMContext):
    await state.update_data(tg_id=msg.from_user.id)
    admin_data = await state.get_data()
    if admin_data['type_of'] == 'Акц':
        admin_data['type_of'] = "Акции и траншевая ипотека"
    data = {'type_of': admin_data['type_of'], 'admin_id': admin_data['tg_id'], 'link': msg.text}
    try:
        async with connect_db() as session:
            res = await create_selection(session, data)
    except:
        await update_selection(session, admin_id=admin_data['tg_id'], type_of=admin_data['type_of'], link=msg.text)
    await msg.answer("Выберите интересующий вас раздел", reply_markup=kb.admin_kb)


@router.callback_query(F.data == "Request_a_consultation_by_phone")
@router.message(UserData.phone_number)
async def menu(msg: Message, state: FSMContext):
    # await msg.message.delete()
    user_data = await state.get_data()
    async with connect_db() as session:
        user = await get_user(session, user_data['id'])
        admin = await get_admin(session, user.admin_id)
        print(user.phone_number)
        try:
            if re.match(r"\+\d{11}", msg.text) or re.match(r"\d{11}", msg.text):
                await update_user(session, user.tg_id, phone_number=msg.text)
                user = await get_user(session, user_data['id'])
        except Exception as e:
            print(e)
    if user.phone_number is None:
        await state.set_state(UserData.phone_number)
        try:
            await msg.message.answer(
                "Введите свой номер телефона для последующего звонка от риелтора(Пример: +71234567890)",
                reply_markup=kb.exit_to_menu_kb)
        except:
            await msg.answer(
                "Введите свой номер телефона для последующего звонка от риелтора(Пример: +71234567890)",
                reply_markup=kb.exit_to_menu_kb)
    else:
        res = send_email(to_email=admin.email, subject='Пришла заявка на консультацию по телефону',
                         message=f'Данные пользователя: {prettify_dict_str(user_data)},\nКонтактный телефон - '
                                 f'{user.phone_number if user.phone_number is not None else msg.text}')
        try:
            await msg.message.answer("Ваш запрос передан риелтору")
            await msg.message.answer("Выберите интересующий вас раздел", reply_markup=kb.menu)
        except:
            await msg.answer("Ваш запрос передан риелтору")
            await msg.answer("Выберите интересующий вас раздел", reply_markup=kb.menu)


class Question(StatesGroup):
    question = State()


@router.message(Question.question)
async def menu(msg: Message, state: FSMContext):
    # await msg.delete()
    user_data = await state.get_data()
    async with connect_db() as session:
        user = await get_user(session, user_data['id'])
        admin = await get_admin(session, user.admin_id)
    res = send_email(to_email=admin.email, subject='Пришел вопрос от пользователя',
                     message=f'Данные пользователя: {prettify_dict_str(user_data)},\nВопрос - {msg.text}')
    await msg.answer("Ваш вопрос передан риелтору")
    await msg.answer("Выберите интересующий вас раздел", reply_markup=kb.menu)


@router.callback_query(F.data == "Ask_your_question")
async def menu(msg: Message, state: FSMContext):
    await msg.message.delete()
    await state.set_state(Question.question)
    await msg.message.answer("Введите свой вопрос:", reply_markup=kb.exit_to_menu_kb)


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
            , reply_markup=kb.exit_to_menu_kb)
    elif data[1] == '2':
        await callback_query.message.answer(
            f"*высылать ссылку на подборку*: "
            , reply_markup=kb.exit_to_menu_kb)
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
            , reply_markup=kb.exit_to_menu_kb)
    elif data[1] == '2':
        await callback_query.message.answer(
            f"*высылать ссылку на подборку*: "
            , reply_markup=kb.exit_to_menu_kb)
    else:
        await callback_query.message.answer(
            f"*высылать ссылку на подборку*: "
            , reply_markup=kb.exit_to_menu_kb)


# default way of displaying a selector to user - date set for today
@router.callback_query(F.data == "sell_real_estate")
async def sell_real_estate(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserData.NAME)

    await callback_query.message.delete()
    await callback_query.message.answer(
        "Вы хотите указать только тип объекта либо же дополнительно рассчитать его стоимость?",
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
    await callback_query.message.answer('Введите адрес объекта.\nПример: г. Москва ул. Автомоторная д 5 кв 13',
                                        reply_markup=kb.exit_to_menu_kb)


@router.message(SellPattern.ADDRESS)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    user_data = await state.get_data()
    if user_data['IS_TRUE'] != "True":
        await type_of_object_final(message, state)
    else:
        await state.set_state(SellPattern.SQUARE)
        # await message.delete()
        await message.answer("Введите площадь объекта в квадратных метрах.\nПример: 50",
                             reply_markup=kb.exit_to_menu_kb)


@router.message(SellPattern.SQUARE)
async def get_birth_date(message: types.Message, state: FSMContext):
    await state.update_data(square=message.text)
    await state.set_state(SellPattern.NUMBER_OF_ROOMS)
    # await message.delete()
    await message.answer("Введите количество комнат.\nПример: 3", reply_markup=kb.exit_to_menu_kb)


@router.message(SellPattern.NUMBER_OF_ROOMS)
async def type_of_object_final(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['IS_TRUE'] == "True":
        await state.update_data(number_of_rooms=message.text)
    user_data = await state.get_data()
    await state.clear()
    async with connect_db() as session:
        print(user_data['id'])
        user = await get_user(session, user_data['id'])
        print(user.admin_id)
        admin = await get_admin(session, user.admin_id)
        print(admin.tg_id)
        print(admin.email)
    print(admin.email)
    res = send_email(to_email=admin.email, subject='Пришла заявка на продажу',
                     message=f'Данные пользователя: {prettify_dict_str(user_data)}')
    print(res)
    await message.answer(
        f"В ближайшее время Вам будет направлена примерная стоимость вашей недвижимости"
    )
    await message.answer("Выберите интересующий вас раздел", reply_markup=kb.menu)

# @router.message()
# async def unhandled_message(message: types.Message):
#     print(message.text)
#     await message.answer("Извините, я не могу обработать этот запрос. Пожалуйста, попробуйте что-нибудь другое.")
