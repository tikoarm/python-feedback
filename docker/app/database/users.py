import logging

from cache.admin import update_admins
from database.connection import get_connection


async def add_user_to_db(telegram_id: int, name: str, source: str):
    prefix = "source_"
    if source and source.startswith(prefix):
        source = source[len(prefix) :]
        source = source.replace("_", ".")
    else:
        source = "Unknown"

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (telegram_id, name, source) VALUES (%s, %s, %s)",
            (
                telegram_id,
                name,
                source,
            ),
        )
        conn.commit()
        logging.info(f"✅ User {telegram_id} ({name}) registered successfully.")
        return True

    except Exception as e:
        logging.error(f"❌ Failed to register user {telegram_id}: {e}")
        return False

    finally:
        cursor.close()
        conn.close()


async def get_internal_user_id(telegram_id: int) -> int | None:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        cursor.close()
        conn.close()


async def get_user_name_by_telegramid(telegram_id: int) -> str | None:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM users WHERE telegram_id = %s", (telegram_id,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        cursor.close()
        conn.close()


async def load_admins():
    conn = get_connection()
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
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT u.*, (
                SELECT COUNT(*) FROM reviews r WHERE r.userid = u.id
            ) AS review_count
            FROM users u
            WHERE u.telegram_id = %s
            LIMIT 1
        """,
            (user_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
