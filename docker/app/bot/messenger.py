import logging

_bot = None


def init_bot(bot_instance):
    global _bot
    _bot = bot_instance


async def send_message_safe(user_id: int, text: str, **kwargs):
    if _bot is None:
        logging.warning(
            (
                "[MESSENGER] Bot is not initialized — "
                f"message to {user_id} not sent."
            )
        )
        return
    result = await _bot.send_message(user_id, text, **kwargs)
    return result


async def remove_markup_safe(user_id: int, message_id: int):
    if _bot is None:
        logging.warning(
            (
                "[MESSENGER] Bot is not initialized — "
                f"removing markups to {user_id} are not possible."
            )
        )
        return
    try:
        await _bot.edit_message_reply_markup(
            chat_id=user_id, message_id=message_id, reply_markup=None
        )
    except Exception as e:
        if "Message is not modified" not in str(e):
            logging.warning(f"[MESSENGER] Failed to remove markup: {e}")
