from aiogram import Bot
from aiogram.enums import ChatMemberStatus


def check_sub_channel(chat_member):
    if chat_member.status != ChatMemberStatus.LEFT:
        return True
    else:
        return False


async def is_channel(bot: Bot, user_id: int, channels: tuple):
    for _, ch_id in channels:
        if not check_sub_channel(await bot.get_chat_member(chat_id=ch_id, user_id=user_id)):
            return False
    return True
