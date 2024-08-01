from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from routers.user_module.user_kb import user_fields
user_router = Router()


@user_router.callback_query(F.data == "fill_user_data")
async def user_menu(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(f"Выберите желаемое действие(В разработке)", reply_markup=user_fields)
