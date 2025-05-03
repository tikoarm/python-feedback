import sys
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

import mysql.connector
from cache.admin import update_admins

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

async def load_admins():
    print("Loading admin list...")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT telegram_id FROM users WHERE admin = 1")
        rows = cursor.fetchall()
        admin_list = [row[0] for row in rows]
    finally:
        cursor.close()
        conn.close()
        print(f"Successfully loaded {len(admin_list)} admins")

    await update_admins(admin_list)

async def get_user_profile(user_id: int):
    conn = get_connection()
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