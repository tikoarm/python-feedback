from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.keyboard import get_ratestars_keyboard
from bot.telegram_bot import bot, dp
import logging
from database.reviews import get_latest_user_review, save_review
from database.users import get_user_name_by_telegramid
from logic.functions import convert_number_to_stars, format_date
from aiogram.utils.markdown import hlink
from dotenv import load_dotenv
import os
from web.gemini import call_gemini, generate_gemini_review_answer

load_dotenv()
user_ratings = {}
waiting_for_review = set()
last_buttons = {}

async def process_add_review(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await start_review_foruser(callback_query.from_user.id)

async def start_review_foruser(userid):
    sent = await bot.send_message(userid, "On a scale of 1 to 5, how satisfied were you?", 
        reply_markup=get_ratestars_keyboard(), parse_mode="Markdown")
    
    set_last_button_message(userid, sent.message_id)
    
async def process_review_stars(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)

    user_id = callback_query.from_user.id
    rating = callback_query.data.split("_")[1]

    user_ratings[user_id] = rating
    waiting_for_review.add(user_id)

    await bot.send_message(callback_query.from_user.id, f"\
    ✅ You rated the restaurant with *{rating} ⭐*\n"
    "Your feedback matters! Tell us what you thought about your visit.", 
        parse_mode="Markdown")
    
@dp.message_handler(lambda message: message.from_user.id in waiting_for_review and not message.text.startswith("/"))
async def process_text_review(message: types.Message):
    user_id = message.from_user.id

    if user_id in waiting_for_review:
        review_text = message.text
        rating = user_ratings.get(user_id)
        name = await get_user_name_by_telegramid(user_id)

        gemini_request = await generate_gemini_review_answer(name, rating, review_text)
        gemini = await call_gemini(gemini_request)
        reviewid = await save_review(user_id, rating, review_text, gemini)

        await bot.send_message(user_id, f"🙏 Thank you for your feedback!\nReview ID: {reviewid}\n\n{gemini}")
        await cancel_rate_progress_global(user_id, False, False)
    
async def process_review_cancel(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await cancel_rate_progress_global(callback_query.from_user.id, True)

async def cancel_rate_progress_global(user_id, with_text=False, with_button=True):
    waiting_for_review.discard(user_id)
    user_ratings.pop(user_id, None)

    if with_button == True: 
        await clear_last_buttons(user_id)

    if with_text == True:
        await bot.send_message(user_id, "❌ Review submission canceled. You can start over at any time.")

def set_last_button_message(user_id: int, message_id: int):
    last_buttons[user_id] = message_id

async def clear_last_buttons(user_id):
    message_id = last_buttons.get(user_id)
    if message_id:
        try:
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=None)
        except Exception as e:
            logging.warning(f"Unable to delete the button at clear_last_buttons: {e}")
        last_buttons.pop(user_id, None)

async def show_last_review(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    user_id = callback_query.from_user.id

    review = await get_latest_user_review(user_id)
    if review == None or not review.get("r_id"):
        bot_username = os.getenv("TG_BOT_USERNAME")
        link = f"https://t.me/{bot_username}?start=addreview"
        text = (
            "It looks like you haven’t written a review yet.\n"
            f"Once you do, you’ll be able to view it {hlink('here', link)}."
        )
        await bot.send_message(user_id, text, parse_mode="HTML")
        return
    
    stars = convert_number_to_stars(int(review['r_stars']))
    date = format_date(review['r_date'])
    text = (
        "*Your most recent review:*\n\n"
        f"*Review ID:* {review['r_id']}\n"
        f"*Review Starter:* {review['u_name']}\n"
        f"*Review Stars:* {stars}\n"
        f"*Review Text:* {review['r_text']}\n"
        f"*Review Date:* {date}\n\n"
        f"*AI Response:* {review['r_ai_answer']}"
    )

    if review['a_text']:
        date = format_date(review['a_date'])
        text += (
            "\n\n"
            f"*Reply from Admin ({review['a_name']} #{review['r_userid']}) – {date}:*\n"
            f"{review['a_text']}"
        )
    await bot.send_message(user_id, text, parse_mode="Markdown")

def register_profile_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(process_add_review, lambda c: c.data == "add_review")
    dp.register_callback_query_handler(process_review_stars, lambda c: c.data.startswith("ratestar_"))
    dp.register_callback_query_handler(process_review_cancel, lambda c: c.data.startswith("review_cancel"))
    dp.register_callback_query_handler(show_last_review, lambda c: c.data.startswith("my_last_review"))