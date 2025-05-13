import logging

from database.connection import get_connection
from database.users import get_internal_user_id
from logic.functions import convert_number_to_stars, format_date


async def save_review(
    user_id: int, rating: int, text: str, ai_response: str
) -> int | None:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        internal_user_id = await get_internal_user_id(user_id)
        if not internal_user_id:
            logging.warning(
                (
                    f"[SAVE_REVIEW] User {user_id} attempted to submit"
                    " a review but is not registered."
                )
            )
            return

        cursor.execute(
            (
                "INSERT INTO reviews (userid, stars, text, ai_answer)"
                " VALUES (%s, %s, %s, %s)"
            ),
            (internal_user_id, rating, text, ai_response),
        )
        conn.commit()
        review_id = cursor.lastrowid
        return review_id
    except Exception as e:
        logging.error(f"❌ Failed to save review: {e}", exc_info=True)
        return None
    finally:
        cursor.close()
        conn.close()


async def get_latest_user_review(telegram_id: int) -> dict | None:
    conn = get_connection()
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
                r.ai_answer AS r_ai_answer,

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
            (telegram_id,),
        )
        row = cursor.fetchone()
        if row:
            return {
                "r_id": row[0],
                "r_userid": row[1],
                "r_stars": row[2],
                "r_text": row[3],
                "r_date": row[4],
                "r_ai_answer": row[5],
                "u_name": row[6],
                "a_adminid": row[7],
                "a_text": row[8],
                "a_date": row[9],
                "a_name": row[10],
            }
        return None
    except Exception as e:
        logging.error(f"❌ Failed to fetch latest review: {e}", exc_info=True)
        return None
    finally:
        cursor.close()
        conn.close()


async def get_all_reviews() -> list[dict] | None:
    conn = get_connection()
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
                r.ai_answer AS r_ai_answer,

                u.name AS u_name,

                a.admin_id AS a_adminid,
                a.text AS a_text,
                a.date AS a_date,

                admin.name AS a_name

            FROM reviews r
            LEFT JOIN users u ON r.userid = u.id
            LEFT JOIN answer a ON a.review_id = r.id
            LEFT JOIN users admin ON admin.id = a.admin_id

            ORDER BY r.id DESC
            """
        )
        rows = cursor.fetchall()
        reviews = []
        for row in rows:
            reviews.append(
                {
                    "r_id": row[0],
                    "r_userid": row[1],
                    "r_stars": convert_number_to_stars(row[2]),
                    "r_text": row[3],
                    "r_date": format_date(row[4]),
                    "r_ai_answer": row[5],
                    "u_name": row[6],
                    "a_adminid": row[7],
                    "a_text": row[8],
                    "a_date": format_date(row[9]),
                    "a_name": row[10],
                }
            )
        return reviews
    except Exception as e:
        logging.error(f"❌ Failed to fetch all reviews: {e}", exc_info=True)
        return None
    finally:
        cursor.close()
        conn.close()


async def get_user_reviews(userid) -> list[dict] | None:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
            SELECT
                r.id AS r_id,
                r.userid AS r_userid,
                r.stars AS r_stars,
                r.text AS r_text,
                r.date AS r_date,
                r.ai_answer AS r_ai_answer,

                u.name AS u_name,

                a.admin_id AS a_adminid,
                a.text AS a_text,
                a.date AS a_date,

                admin.name AS a_name

            FROM reviews r
            LEFT JOIN users u ON r.userid = u.id
            LEFT JOIN answer a ON a.review_id = r.id
            LEFT JOIN users admin ON admin.id = a.admin_id

            WHERE r.userid = %s
            ORDER BY r.id DESC
            """
    cursor.execute(query, (userid,))
    try:
        rows = cursor.fetchall()
        reviews = []
        for row in rows:
            reviews.append(
                {
                    "r_id": row[0],
                    "r_userid": row[1],
                    "r_stars": convert_number_to_stars(row[2]),
                    "r_text": row[3],
                    "r_date": format_date(row[4]),
                    "r_ai_answer": row[5],
                    "u_name": row[6],
                    "a_adminid": row[7],
                    "a_text": row[8],
                    "a_date": format_date(row[9]),
                    "a_name": row[10],
                }
            )
        return reviews
    except Exception as e:
        logging.error(f"❌ Failed to fetch all reviews: {e}", exc_info=True)
        return None
    finally:
        cursor.close()
        conn.close()


async def get_global_stats() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Total number of reviews and average rating
        cursor.execute("SELECT COUNT(*), AVG(stars) FROM reviews")
        total_count, avg_rating = cursor.fetchone()
        sql_select = (
            "SELECT COUNT(*), AVG(stars) FROM reviews WHERE date >= NOW()"
        )

        # In the last day
        cursor.execute(f"{sql_select} - INTERVAL 1 DAY")
        day_count, day_avg = cursor.fetchone()

        # In the last week
        cursor.execute(f"{sql_select} - INTERVAL 7 DAY")
        week_count, week_avg = cursor.fetchone()

        # In the last month
        cursor.execute(f"{sql_select} - INTERVAL 30 DAY")
        month_count, month_avg = cursor.fetchone()

        # Latest review (with user name and answer if available)
        cursor.execute(
            """
            SELECT
                r.stars, r.text, r.date, r.ai_answer,
                u.name,
                a.text, a.date, admin.name
            FROM reviews r
            JOIN users u ON u.id = r.userid
            LEFT JOIN answer a ON a.review_id = r.id
            LEFT JOIN users admin ON admin.id = a.admin_id
            ORDER BY r.id DESC
            LIMIT 1
        """
        )
        row = cursor.fetchone()
        last_review = None
        if row:
            last_review = {
                "stars": convert_number_to_stars(row[0]),
                "text": row[1],
                "date": format_date(row[2]),
                "ai_answer": row[3],
                "user_name": row[4],
                "admin_answer": row[5],
                "admin_answer_date": format_date(row[6]) if row[6] else None,
                "admin_name": row[7],
            }

        return {
            "total_reviews": total_count,
            "average_rating": round(avg_rating or 0, 2),
            "day_count": day_count or 0,
            "day_avg": round(day_avg or 0, 2),
            "week_count": week_count or 0,
            "week_avg": round(week_avg or 0, 2),
            "month_count": month_count or 0,
            "month_avg": round(month_avg or 0, 2),
            "last_review": last_review,
        }
    except Exception as e:
        logging.error(f"❌ Failed to fetch global stats: {e}", exc_info=True)
        return {}
    finally:
        cursor.close()
        conn.close()
