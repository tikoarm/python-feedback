import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from database.users import get_user_profile
from cache.admin import is_admin
from bot.keyboard import get_profile_keyboard
from web.gemini import call_gemini, generate_gemini_review_answer

load_dotenv()
tg_token = os.getenv('TG_TOKEN')
bot = Bot(token=tg_token)
dp = Dispatcher(bot)

from bot.handlers.profile_handler import register_profile_handlers, set_last_button_message, cancel_rate_progress_global, start_review_foruser
register_profile_handlers(dp)

import time
@dp.message_handler(commands=['test'])
async def cmd_test(message: types.Message):
    stars = 5
    name = "Мария К."
    text = "Отличное место! Всё было очень вкусно, особенно десерты. Обслуживание на высоте."
    gemini_request = await generate_gemini_review_answer(name, stars, text)
    gemini = await call_gemini(gemini_request)
    await bot.send_message(message.from_user.id, f"Review:\nStar: {stars}\nName: {name}\nText: {text}\n\nResult:\n{gemini}")
    
    stars = 2
    name = "Игорь С."
    text = "Еда посредственная, а ждать заказ пришлось почти час. Вряд ли вернусь снова."
    gemini_request = await generate_gemini_review_answer(name, stars, text)
    gemini = await call_gemini(gemini_request)
    await bot.send_message(message.from_user.id, f"Review:\nStar: {stars}\nName: {name}\nText: {text}\n\nResult:\n{gemini}")

    stars = 1
    name = "Анна Л."
    text = "Во время нашей свадьбы произошла драка в соседнем банковском зале со стрельбой, наш праздник испорчен!"
    gemini_request = await generate_gemini_review_answer(name, stars, text)
    gemini = await call_gemini(gemini_request)
    await bot.send_message(message.from_user.id, f"Review:\nStar: {stars}\nName: {name}\nText: {text}\n\nResult:\n{gemini}")

    stars = 5
    name = "Алексей Л."
    text = "Отдыхаем у вас регулярно, все замечательно. Недавно посоветовал своему другу провести у вас свой день рождения, он тоже остался доволен!"
    gemini_request = await generate_gemini_review_answer(name, stars, text)
    gemini = await call_gemini(gemini_request)
    await bot.send_message(message.from_user.id, f"Review:\nStar: {stars}\nName: {name}\nText: {text}\n\nResult:\n{gemini}")

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    tg_id = message.from_user.id
    args = message.get_args()
    
    if args == "addreview":
        await start_review_foruser(tg_id)
        return
    
    result = f"Hi!\nYour ID is: {tg_id}"
    if await is_admin(tg_id):
        result += f"\nYou are admin"
    await bot.send_message(message.from_user.id, result)

@dp.message_handler(commands=['profile'])
async def cmd_profile(message: types.Message):
    user_id = message.from_user.id
    user_data = await get_user_profile(user_id)

    if not user_data:
        await message.reply("❌ Profile not found.")
        return
    
    await cancel_rate_progress_global(message.from_user.id)

    status = "Admin" if int(user_data['admin']) == 1 else "User"
    text = (
        f"👤 My Profile:\n\n"
        f"💎 Name: *{user_data['name']}* 💎\n"
        f"📝 Number of reviews: *{user_data['review_count']}* 📝\n"
        f"🔧 Join date: *{user_data['reg_date']}* 🔧\n"
        f"🔧 Status: *{status}* 🔧\n"
    )
    sent = await bot.send_message(message.from_user.id, text, reply_markup=get_profile_keyboard(), parse_mode="Markdown")
    set_last_button_message(message.from_user.id, sent.message_id)

async def start():
    await dp.start_polling()