import os

import requests
from aiogram import types
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

from bot.handlers.profile_handler import set_last_button_message
from bot.keyboard import global_admins_buttons
from bot.messenger import send_message_safe
from cache.admin import is_admin
from cache.api_keys import db_get_all_api_keys, db_is_valid_api_key
from database.reviews import get_global_stats
from database.users import get_internal_user_id

load_dotenv()
api_admin_key = os.getenv("API_ADMIN_KEY")
api_domain = os.getenv("API_DOMAIN")
if not api_admin_key or not api_domain:
    raise ValueError("Missing API credentials in environment variables.")


def register_admin_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        process_show_admin_panel, lambda c: c.data == "show_admin_panel"
    )
    dp.register_callback_query_handler(
        process_admin_info, lambda c: c.data == "admin_info"
    )
    dp.register_callback_query_handler(
        process_api_keys, lambda c: c.data == "admin_show_all_api"
    )
    dp.register_callback_query_handler(
        process_create_api, lambda c: c.data == "admin_create_api_key"
    )
    dp.register_callback_query_handler(
        process_admin_close, lambda c: c.data == "process_admin_close"
    )


async def process_admin_close(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)


async def process_create_api(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)

    if not await is_admin(callback_query.from_user.id):
        await send_message_safe(
            callback_query.from_user.id,
            "You don't have permission to use this command!",
            parse_mode="Markdown",
        )
        return

    try:
        internal_user_id = await get_internal_user_id(callback_query.from_user.id)
        response = requests.post(
            f"{api_domain}/apikey/add",
            params={"admin_key": api_admin_key, "user_id": internal_user_id},
            timeout=5,
        )
        if response.status_code == 200:
            api_key = response.json().get("api_key")
            await send_message_safe(
                callback_query.from_user.id,
                f"Generated API key:\n{api_key}",
                parse_mode="Markdown",
            )
        else:
            await send_message_safe(
                callback_query.from_user.id,
                "Failed to generate API key.",
                parse_mode="Markdown",
            )
    except Exception as e:
        await send_message_safe(
            callback_query.from_user.id, f"Error: {e}", parse_mode="Markdown"
        )


async def process_api_keys(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)

    if not await is_admin(callback_query.from_user.id):
        await send_message_safe(
            callback_query.from_user.id,
            "You don't have permission to use this command!",
            parse_mode="Markdown",
        )
        return

    all_api_str = await db_get_all_api_keys()
    await send_message_safe(
        callback_query.from_user.id,
        "All bot's API keys:\n" + all_api_str,
        parse_mode="Markdown",
    )


async def process_admin_info(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)

    if not await is_admin(callback_query.from_user.id):
        return 0

    stats = await get_global_stats()
    lr = stats["last_review"]

    text = (
        "📊 *Global Stats*\n\n"
        f"🗂 Total reviews: {stats['total_reviews']}\n"
        f"⭐️ Average rating: {stats['average_rating']}\n\n"
        f"🕒 Reviews today: {stats['day_count']} (avg: {stats['day_avg']})\n"
        f"📅 Reviews this week: {stats['week_count']} (avg: {stats['week_avg']})\n"
        f"🗓 Reviews this month: {stats['month_count']} (avg: {stats['month_avg']})\n"
    )

    if lr:
        text += (
            "\n\n📝 *Last review*:\n"
            f"👤 User: {lr['user_name']}\n"
            f"⭐️ {lr['stars']}\n"
            f"🗓 {lr['date']}\n"
            f"💬 {lr['text']}\n"
            f"🤖 AI: {lr['ai_answer']}\n"
        )
        if lr["admin_answer"]:
            text += f"\n👮‍♂️ Admin ({lr['admin_name']}): {lr['admin_answer']} ({lr['admin_answer_date']})"

    await send_message_safe(callback_query.from_user.id, text, parse_mode="Markdown")


async def process_show_admin_panel(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_reply_markup(reply_markup=None)

    if not await is_admin(callback_query.from_user.id):
        return 0

    sent = await send_message_safe(
        callback_query.from_user.id,
        "Please, select action...",
        reply_markup=global_admins_buttons(),
        parse_mode="Markdown",
    )
    set_last_button_message(callback_query.from_user.id, sent.message_id)
