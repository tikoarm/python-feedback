import sys
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

#tg_token = os.getenv('')

async def is_user_admin(userid):
    return True