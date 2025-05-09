from datetime import datetime
import logging

def convert_number_to_stars(number):
    max_stars = 5
    text = ""

    for i in range(1, max_stars + 1):
        if number >= i:
            text += "⭐"
        else:
            text += "☆"

    return text

def format_date(date_str: str | datetime) -> str:
    try:
        if isinstance(date_str, datetime):
            dt = date_str
        else:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except Exception as e:
        logging.error(f"Invalid date: {date_str}")
        return "Invalid date"
    
    return dt.strftime("%B %-d, %Y, %H:%M")

def get_tg_faq_text():
    text = (
        "<b>🤖 FAQ</b>\n\n"
        "<b>/profile</b> — Main bot page. From here you can:\n"
        "• Access the admin panel (if you're an admin)\n"
        "• Write a new review\n"
        "• View your latest review\n"
        "/check_apikey - Check API key availability\n\n"
        "<b>👨‍💻 For developers:</b>\n\n"
        '📄 localhost:5050/review_list/?user=all | JSON: All reviews\n'
        '📄 localhost:5050/review_list/?user=input_userid_here | JSON: Reviews by user ID\n\n'

        '🌐 localhost:8888/reviews.php?user=all | Web: All reviews\n'
        '🌐 localhost:8888/reviews.php?user=input_userid_here | Web: Reviews by user ID\n'
    )
    return text