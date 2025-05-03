from aiogram import types
from aiogram.dispatcher import Dispatcher

async def process_add_review(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("✍️ Write your review:")

def register_profile_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(process_add_review, lambda c: c.data == "add_review")