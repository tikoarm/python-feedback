import asyncio

_admin_set = set()

async def update_admins(admin_list: list[int]):
    global _admin_set
    _admin_set = set(admin_list)

async def is_admin(user_id: int) -> bool:
    return user_id in _admin_set

async def add_admin(user_id: int):
    _admin_set.add(user_id)