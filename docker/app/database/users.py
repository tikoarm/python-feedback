import sys
import os
import asyncio
import logging
from cache.admin import update_admins

from database.connection import get_connection

async def load_admins():
    conn = await get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT telegram_id FROM users WHERE admin = 1")
        rows = cursor.fetchall()
        admin_list = [row[0] for row in rows]
    finally:
        cursor.close()
        conn.close()
        logging.info(f"Successfully loaded {len(admin_list)} admins")

    await update_admins(admin_list)

async def get_user_profile(user_id: int):
    conn = await get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT u.*, (
                SELECT COUNT(*) FROM reviews r WHERE r.userid = u.id
            ) AS review_count
            FROM users u
            WHERE u.telegram_id = %s
            LIMIT 1
        """, (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()