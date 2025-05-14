import logging
from datetime import datetime


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
    except Exception:
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
        "🌐 feedback.tikoarm.com/localhost.php"
    )
    return text


def format_seconds(seconds: int) -> str:
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if secs > 0 or not parts:
        parts.append(f"{secs} second{'s' if secs != 1 else ''}")

    return ", ".join(parts)

