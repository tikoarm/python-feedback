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