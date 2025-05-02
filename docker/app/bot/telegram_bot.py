import sys
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher, types

sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))
import users
from users import is_user_admin

tg_token = os.getenv('TG_TOKEN')
bot = Bot(token=tg_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    tg_id = message.from_user.id
    
    result = f"Hi!\nYour ID is: {tg_id}"
    if is_user_admin(tg_id):
        result += f"You are admin"
    await bot.send_message(message.from_user.id, result, reply_markup=keyboard)

async def start():
    await dp.start_polling()