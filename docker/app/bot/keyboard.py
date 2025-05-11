from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_profile_keyboard(is_admin: int):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="➕ Add Review", callback_data="add_review"),
        InlineKeyboardButton(text="⭐️ My Last Review", callback_data="my_last_review"),
        InlineKeyboardButton(text="🚫 Cancel 🚫", callback_data="review_cancel"),
    )

    if is_admin == 1:
        keyboard.add(
            InlineKeyboardButton(text="💎 Admin 💎", callback_data="show_admin_panel")
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
        InlineKeyboardButton(text="🚫 Cancel 🚫", callback_data="review_cancel"),
    )
    return keyboard


def global_admins_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="📝 Global Information 📝", callback_data="admin_info"
        ),
        InlineKeyboardButton(
            text="🛰️ Show API Keys 🛰️", callback_data="admin_show_all_api"
        ),
        InlineKeyboardButton(
            text="🛰️ Create API Key 🛰️", callback_data="admin_create_api_key"
        ),
        InlineKeyboardButton(text="🚫 Cancel 🚫", callback_data="process_admin_close"),
    )
    return keyboard
