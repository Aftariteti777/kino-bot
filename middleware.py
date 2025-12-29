from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_all_channels


async def check_user_subscription(bot: Bot, user_id: int):
    """Check if user is subscribed to all mandatory channels"""
    channels = await get_all_channels()
    
    if not channels:
        return True, None
    
    not_subscribed = []
    
    for channel in channels:
        try:
            member = await bot.get_chat_member(chat_id=channel['channel_id'], user_id=user_id)
            if member.status in ['left', 'kicked']:
                not_subscribed.append(channel)
        except Exception:
            not_subscribed.append(channel)
    
    if not_subscribed:
        return False, not_subscribed
    
    return True, None


def get_subscription_keyboard(channels):
    """Generate keyboard with subscription buttons"""
    keyboard = []
    
    for channel in channels:
        channel_name = channel['channel_username'] if channel['channel_username'] else channel['channel_id']
        if channel_name.startswith('@'):
            url = f"https://t.me/{channel_name[1:]}"
        else:
            url = f"https://t.me/{channel_name}"
        
        keyboard.append([InlineKeyboardButton(
            text=f"📢 {channel_name}",
            url=url
        )])
    
    keyboard.append([InlineKeyboardButton(
        text="✅ Tekshirish",
        callback_data="check_subscription"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
