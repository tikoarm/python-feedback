import secrets
from database.connection import get_connection
import logging

api_keys_cache = set()


async def generate_api_key(user_id):
    while True:
        new_key = secrets.token_hex(16)
        if new_key not in api_keys_cache:
            api_keys_cache.add(new_key)
            await db_add_api_key(new_key, user_id)
            return new_key


def is_valid_api_key(api_key):
    return api_key in api_keys_cache


async def load_api_keys():
    conn = await get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT api_key FROM api_keys")
        rows = cursor.fetchall()
        keys = [row[0] for row in rows]
        for key in keys:
            api_keys_cache.add(key)
    finally:
        cursor.close()
        conn.close()
        logging.info(f"Successfully loaded {len(keys)} API keys")


# Telegram Functions
async def db_add_api_key(api_key: str, user_id: int) -> None:
    conn = await get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO api_keys (api_key, created_by) VALUES (%s, %s)",
            (
                api_key,
                user_id,
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


async def db_get_all_api_keys():
    conn = await get_connection()
    cursor = conn.cursor()

    text = []
    try:
        cursor.execute("SELECT api_key FROM api_keys")
        rows = cursor.fetchall()
        keys = [row[0] for row in rows]

        for i, key in enumerate(keys, start=1):
            text.append(f"{i}. {key}")

    finally:
        cursor.close()
        conn.close()

    return "\n".join(text)


async def db_is_valid_api_key(api_key: str) -> bool:
    conn = await get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT 1 FROM api_keys WHERE api_key = %s LIMIT 1", (api_key,))
        result = cursor.fetchone()
        return result is not None

    finally:
        cursor.close()
        conn.close()
