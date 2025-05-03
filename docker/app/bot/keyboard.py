from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_profile_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="➕ Add Review", callback_data="add_review")
    )
    return keyboard