from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard(is_admin=False):
    """Main keyboard for users"""
    if is_admin:
        keyboard = [
            [KeyboardButton(text="👨‍💼 Admin Panel")]
        ]
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return None


def get_admin_keyboard():
    """Admin panel main keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats"),
            InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="admin_add_channel")
        ],
        [
            InlineKeyboardButton(text="📋 Kanallar ro'yxati", callback_data="admin_list_channels"),
            InlineKeyboardButton(text="🗑 Kanal o'chirish", callback_data="admin_delete_channel")
        ],
        [
            InlineKeyboardButton(text="➕ Kino qo'shish", callback_data="admin_add_movie"),
            InlineKeyboardButton(text="🗑 Kino o'chirish", callback_data="admin_delete_movie")
        ],
        [
            InlineKeyboardButton(text="📢 Xabar yuborish", callback_data="admin_broadcast"),
            InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton(text="❌ Yopish", callback_data="admin_close")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_channels_keyboard(channels):
    """Channels list keyboard"""
    keyboard = []
    
    for channel in channels:
        channel_name = channel['channel_username'] if channel['channel_username'] else channel['channel_id']
        keyboard.append([
            InlineKeyboardButton(
                text=f"❌ {channel_name}",
                callback_data=f"delete_channel_{channel['id']}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton(text="🔙 Ortga", callback_data="admin_panel")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_keyboard():
    """Back button keyboard"""
    keyboard = [[InlineKeyboardButton(text="🔙 Ortga", callback_data="admin_panel")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_cancel_keyboard():
    """Cancel button keyboard"""
    keyboard = [[InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
