from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.keyboard import get_ratestars_keyboard
from bot.telegram_bot import bot

user_ratings = {}
waiting_for_review = set()
last_buttons = {}

async def process_add_review(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    sent = await bot.send_message(callback_query.from_user.id, "On a scale of 1 to 5, how satisfied were you?", 
        reply_markup=get_ratestars_keyboard(), parse_mode="Markdown")
    
    set_last_button_message(callback_query.from_user.id, sent.message_id)
    
async def process_review_stars(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)

    user_id = callback_query.from_user.id
    rating = callback_query.data.split("_")[1]

    user_ratings[user_id] = rating
    waiting_for_review.add(user_id)
    await bot.send_message(callback_query.from_user.id, f"\
    ✅ You rated the restaurant with *{rating} ⭐*\n\
    Your feedback matters! Tell us what you thought about your visit.", 
        parse_mode="Markdown")
    
async def process_review_cancel(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await cancel_rate_progress_global(callback_query.from_user.id, True)

async def cancel_rate_progress_global(user_id, with_text=False):
    waiting_for_review.discard(user_id)
    user_ratings.pop(user_id, None)
    await clear_last_buttons(user_id)

    if with_text == True:
        await bot.send_message(user_id, "❌ Review submission canceled. You can start over at any time.")

def register_profile_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(process_add_review, lambda c: c.data == "add_review")
    dp.register_callback_query_handler(process_review_stars, lambda c: c.data.startswith("ratestar_"))
    dp.register_callback_query_handler(process_review_cancel, lambda c: c.data.startswith("review_cancel"))

def set_last_button_message(user_id: int, message_id: int):
    last_buttons[user_id] = message_id

async def clear_last_buttons(user_id):
    message_id = last_buttons.get(user_id)
    if message_id:
        try:
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=None)
        except Exception as e:
            print(f"Unable to delete the button at clear_last_buttons: {e}")
        last_buttons.pop(user_id, None)