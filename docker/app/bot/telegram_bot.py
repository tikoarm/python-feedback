import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from database.users import get_user_profile, add_user_to_db
from cache.admin import is_admin
from bot.keyboard import get_profile_keyboard
from web.gemini import call_gemini, generate_gemini_review_answer

load_dotenv()
tg_token = os.getenv('TG_TOKEN')
bot = Bot(token=tg_token)
dp = Dispatcher(bot)

from bot.handlers.profile_handler import register_profile_handlers, set_last_button_message, cancel_rate_progress_global, start_review_foruser
register_profile_handlers(dp)

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

    result += "\nBot's main menu: /profile"
    await bot.send_message(message.from_user.id, result)

@dp.message_handler(commands=['profile'])
async def cmd_profile(message: types.Message):
    user_id = message.from_user.id
    user_data = await get_user_profile(user_id)

    if not user_data:
        await register_user(message)
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

async def register_user(message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name

    result = await add_user_to_db(telegram_id, name)
    if result == True:
        text = (
            "*Welcome, and thank you for registering! 🎉*\n"
            "We’re excited to have you with us.\n"
            "To start using the bot and set up your profile, just type */profile*.\n\n"
            "Looking forward to hearing your feedback!"
        )
        await bot.send_message(telegram_id, text, parse_mode="Markdown")

async def start():
    await dp.start_polling()