import logging
from database.connection import get_connection

async def save_review(user_id: int, rating: int, text: str) -> int | None:
    conn = await get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO reviews (userid, rating, text) VALUES (%s, %s, %s)",
            (user_id, rating, text)
        )
        conn.commit()
        review_id = cursor.lastrowid
        logging.info(f"✅ Review saved: id={review_id}, user={user_id}, rating={rating}")
        return review_id
    except Exception as e:
        logging.error(f"❌ Failed to save review: {e}", exc_info=True)
        return None
    finally:
        cursor.close()
        conn.close()

async def get_latest_user_review(telegram_id: int) -> dict | None:
    conn = await get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                r.id AS r_id,
                r.userid AS r_userid,
                r.stars AS r_stars,
                r.text AS r_text,
                r.date AS r_date,

                u.name AS u_name,

                a.admin_id AS a_adminid,
                a.text AS a_text,
                a.date AS a_date,

                admin.name AS a_name

            FROM users u
            LEFT JOIN reviews r ON r.userid = u.id
            LEFT JOIN answer a ON a.review_id = r.id
            LEFT JOIN users admin ON admin.id = a.admin_id

            WHERE u.telegram_id = %s
            ORDER BY r.id DESC
            LIMIT 1
            """,
            (telegram_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "r_id": row[0],
                "r_userid": row[1],
                "r_stars": row[2],
                "r_text": row[3],
                "r_date": row[4],
                "u_name": row[5],
                "a_adminid": row[6],
                "a_text": row[7],
                "a_date": row[8],
                "a_name": row[9]
            }
        return None
    except Exception as e:
        logging.error(f"❌ Failed to fetch latest review: {e}", exc_info=True)
        return None
    finally:
        cursor.close()
        conn.close()