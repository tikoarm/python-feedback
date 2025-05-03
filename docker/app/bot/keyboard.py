from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_profile_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="➕ Add Review", callback_data="add_review"),
        InlineKeyboardButton(text="🚫 Cancel 🚫", callback_data="review_cancel")
    )
    return keyboard

def get_ratestars_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="⭐☆☆☆☆", callback_data="ratestar_1"),
        InlineKeyboardButton(text="⭐⭐☆☆☆", callback_data="ratestar_2"),
        InlineKeyboardButton(text="⭐⭐⭐☆☆", callback_data="ratestar_3"),
        InlineKeyboardButton(text="⭐⭐⭐⭐☆", callback_data="ratestar_4"),
        InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data="ratestar_5"),
        InlineKeyboardButton(text="🚫 Cancel 🚫", callback_data="review_cancel")
    )
    return keyboard