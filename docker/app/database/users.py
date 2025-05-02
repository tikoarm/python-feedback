import sys
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

async def is_user_admin(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT admin FROM users WHERE user_id = %s LIMIT 1"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            return bool(result[0])
        return False
    finally:
        cursor.close()
        conn.close()