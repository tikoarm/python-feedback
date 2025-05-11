import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from bot import messenger
from bot.handlers.admin_handler import register_admin_handlers
from bot.handlers.profile_handler import (
    cancel_rate_progress_global,
    process_text_review,
    register_profile_handlers,
    set_last_button_message,
    start_review_foruser,
    waiting_for_review,
)
from bot.keyboard import get_profile_keyboard
from cache.admin import is_admin
from cache.api_keys import db_is_valid_api_key
from database.users import add_user_to_db, get_user_profile
from logic.functions import get_tg_faq_text

load_dotenv()
tg_token = os.getenv("TG_TOKEN")
if not tg_token:
    raise ValueError("Missing Telegram credential in environment variables.")

bot = Bot(token=tg_token)
dp = Dispatcher(bot)

messenger.init_bot(bot)
register_profile_handlers(dp)
register_admin_handlers(dp)


@dp.message_handler(commands=["check_apikey"])
async def cmd_create_api(message: types.Message):
    if not await is_admin(message.from_user.id):
        await bot.send_message(
            message.from_user.id,
            "You don't have permission to use this command!",
            parse_mode="Markdown",
        )
        return
    args = message.get_args()
    if not args:
        await bot.send_message(
            message.from_user.id, "*/check_apikey api_key*", parse_mode="Markdown"
        )
        return

    status = "valid" if await db_is_valid_api_key(args) else "invalid"
    await bot.send_message(
        message.from_user.id, f"API Key `{args}` is *{status}*", parse_mode="Markdown"
    )


@dp.message_handler(commands=["help", "faq"])
async def cmd_help(message: types.Message):
    await bot.send_message(message.from_user.id, get_tg_faq_text(), parse_mode="HTML")


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    tg_id = message.from_user.id
    args = message.get_args()

    user_data = await get_user_profile(tg_id)

    if not user_data:
        await register_user(message, args)
        return

    if args == "addreview":
        await start_review_foruser(tg_id)
        return

    result = f"Hi!\nYour ID is: {tg_id}"
    if await is_admin(tg_id):
        result += "\nYou are admin"

    result += "\nBot's main menu: /profile"
    await bot.send_message(message.from_user.id, result)


@dp.message_handler(commands=["profile"])
async def cmd_profile(message: types.Message):
    user_id = message.from_user.id
    user_data = await get_user_profile(user_id)

    if not user_data:
        await register_user(message)
        return

    await cancel_rate_progress_global(message.from_user.id)

    status = "Admin" if int(user_data["admin"]) == 1 else "User"
    text = (
        f"👤 My Profile:\n\n"
        f"💎 Name: *{user_data['name']}* 💎\n"
        f"📝 Number of reviews: *{user_data['review_count']}* 📝\n"
        f"🔧 Join date: *{user_data['reg_date']}* 🔧\n"
        f"🔧 Status: *{status}* 🔧\n"
    )
    sent = await bot.send_message(
        message.from_user.id,
        text,
        reply_markup=get_profile_keyboard(int(user_data["admin"])),
        parse_mode="Markdown",
    )
    set_last_button_message(message.from_user.id, sent.message_id)


async def register_user(message, args="Unknown"):
    telegram_id = message.from_user.id
    name = message.from_user.full_name

    result = await add_user_to_db(telegram_id, name, args)
    if result:
        text = (
            "*Welcome, and thank you for registering! 🎉*\n"
            "We're excited to have you with us.\n"
            "To start using the bot and set up your profile, just type */profile*.\n\n"
            "Looking forward to hearing your feedback!"
        )
        await bot.send_message(telegram_id, text, parse_mode="Markdown")


@dp.message_handler(
    lambda message: message.from_user.id in waiting_for_review
    and not message.text.startswith("/")
)
async def process_text_review_tg(message: types.Message):
    await process_text_review(message)


async def start():
    await dp.start_polling()
