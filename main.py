import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN, ADMIN_IDS, MESSAGES
from database import (
    init_db, add_user, get_movie_by_code, add_movie, delete_movie,
    add_channel, get_all_channels, delete_channel, get_all_users,
    get_user_count, get_active_user_count, get_movie_count, get_channel_count,
    init_default_channel, add_admin, get_all_admins, delete_admin, is_admin_in_db
)
from middleware import check_user_subscription, get_subscription_keyboard
from keyboards import (
    get_admin_keyboard, get_channels_keyboard, get_back_keyboard, get_cancel_keyboard,
    get_main_keyboard, get_admins_keyboard
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# FSM States
class AdminStates(StatesGroup):
    waiting_for_channel = State()
    waiting_for_broadcast = State()
    waiting_for_movie_code = State()
    waiting_for_movie_file = State()
    waiting_for_movie_title = State()
    waiting_for_delete_code = State()
    waiting_for_admin_id = State()


# Helper function to check if user is admin
async def is_admin(user_id: int) -> bool:
    """Check if user is admin (from config or database)"""
    if user_id in ADMIN_IDS:
        return True
    return await is_admin_in_db(user_id)


# Start command handler
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    await add_user(user.id, user.username, user.first_name, user.last_name)
    
    # Check subscription
    is_subscribed, not_subscribed_channels = await check_user_subscription(bot, user.id)
    
    if not is_subscribed:
        text = MESSAGES["not_subscribed"]
        keyboard = get_subscription_keyboard(not_subscribed_channels)
        await message.answer(text, reply_markupawait =keyboard)
        return
    
    # Show keyboard with admin button if user is admin
    main_keyboard = get_main_keyboard(is_admin=is_admin(user.id))
    await message.answer(MESSAGES["start"], reply_markup=main_keyboard)


# Check subscription callback
@dp.callback_query(F.data == "check_subscription")
async def callback_check_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id
    is_subscribed, not_subscribed_channels = await check_user_subscription(bot, user_id)
    
    if not is_subscribed:
        text = MESSAGES["not_subscribed"]
        keyboard = get_subscription_keyboard(not_subscribed_channels)
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.message.edit_text(MESSAGES["subscribed"])
        main_keyboard = get_main_keyboard(is_admin=await is_admin(user_id))
        await callback.message.answer(MESSAGES["start"], reply_markup=main_keyboard)
    
    await callback.answer()


# Movie request handler - LAST HANDLER (catches all other text)
@dp.message(F.text, StateFilter(None))
async def handle_movie_request(message: Message, state: FSMContext):
    logger.info(f"Movie handler triggered for text: {message.text[:20]}...")
    
    # Check if admin panel button pressed
    if message.text == "👨‍💼 Admin Panel":
        if await is_admin(message.from_user.id):
            keyboard = get_admin_keyboard()
            await message.answer(MESSAGES["admin_panel"], reply_markup=keyboard)
        else:
            await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    user = message.from_user
    await add_user(user.id, user.username, user.first_name, user.last_name)
    
    # Check subscription
    is_subscribed, not_subscribed_channels = await check_user_subscription(bot, user.id)
    
    if not is_subscribed:
        text = MESSAGES["not_subscribed"]
        keyboard = get_subscription_keyboard(not_subscribed_channels)
        await message.answer(text, reply_markup=keyboard)
        return
    
    # Search for movie
    code = message.text.strip()
    movie = await get_movie_by_code(code)
    
    if movie:
        try:
            await message.answer_video(
                video=movie['file_id'],
                caption=f"🎬 {movie['title'] or 'Kino'}\n\n{movie['description'] or ''}"
            )
            await message.answer(MESSAGES["movie_sent"])
        except Exception as e:
            logger.error(f"Error sending movie: {e}")
            await message.answer("❌ Kino yuborishda xatolik yuz berdi.")
    else:
        await message.answer(MESSAGES["movie_not_found"])


# Admin panel command
@dp.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    keyboard = get_admin_keyboard()
    await message.answer(MESSAGES["admin_panel"], reply_markup=keyboard)


# Admin panel callback
@dp.callback_query(F.data == "admin_panel")
async def callback_admin_panel(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    await state.clear()
    keyboard = get_admin_keyboard()
    await callback.message.edit_text(MESSAGES["admin_panel"], reply_markup=keyboard)
    await callback.answer()


# Statistics
@dp.callback_query(F.data == "admin_stats")
async def callback_admin_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    total_users = await get_user_count()
    active_users = await get_active_user_count()
    total_movies = await get_movie_count()
    total_channels = await get_channel_count()
    
    text = MESSAGES["statistics"].format(
        total_users=total_users,
        active_users=active_users,
        total_movies=total_movies,
        total_channels=total_channels
    )
    
    keyboard = get_back_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


# Add channel - start
@dp.callback_query(F.data == "admin_add_channel")
async def callback_add_channel(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    keyboard = get_cancel_keyboard()
    await callback.message.edit_text(MESSAGES["channel_add"], reply_markup=keyboard)
    await state.set_state(AdminStates.waiting_for_channel)
    await callback.answer()


# Add channel - receive channel ID
@dp.message(StateFilter(AdminStates.waiting_for_channel), F.text)
async def process_add_channel(message: Message, state: FSMContext):
    logger.info(f"✅ Channel handler triggered! Received: {message.text}")
    
    if not is_admin(message.from_user.id):
        await state.clear()
        return
    
    channel_input = message.text.strip()
    logger.info(f"Processing channel: {channel_input}")
    
    # Extract channel ID or username
    if channel_input.startswith('@'):
        channel_username = channel_input
        # For username, we need to test if bot can access it
        # We'll use send_chat_action as a lightweight test
        try:
            await bot.send_chat_action(channel_input, "typing")
            # If successful, we can access the channel
            channel_id = channel_input  # Store username as ID for now
            logger.info(f"Successfully verified channel access: {channel_username}")
        except Exception as e:
            logger.error(f"Error accessing channel: {e}")
            await message.answer("❌ Kanalga kirish imkoni yo'q!\n\nBot kanalda admin ekanligini va barcha huquqlarga ega ekanligini tekshiring.")
            await state.clear()
            keyboard = get_admin_keyboard()
            await message.answer(MESSAGES["admin_panel"], reply_markup=keyboard)
            return
    else:
        # If numeric ID is provided
        channel_id = channel_input
        channel_username = None
        
        # Try to verify bot can access the channel
        try:
            await bot.send_chat_action(channel_id, "typing")
            logger.info(f"Successfully verified channel access: {channel_id}")
        except Exception as e:
            logger.error(f"Error accessing channel: {e}")
            await message.answer("❌ Kanalga kirish imkoni yo'q!\n\nKanal ID to'g'ri ekanligini va bot admin ekanligini tekshiring.")
            await state.clear()
            keyboard = get_admin_keyboard()
            await message.answer(MESSAGES["admin_panel"], reply_markup=keyboard)
            return
    
    success = await add_channel(channel_id, channel_username)
    
    if success:
        await message.answer(MESSAGES["channel_added"])
    else:
        await message.answer("❌ Bu kanal allaqachon qo'shilgan!")
    
    await state.clear()
    keyboard = get_admin_keyboard()
    await message.answer(MESSAGES["admin_panel"], reply_markup=keyboard)


# List channels
@dp.callback_query(F.data == "admin_list_channels")
async def callback_list_channels(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    channels = await get_all_channels()
    
    if not channels:
        text = "📋 Majburiy kanallar yo'q."
        keyboard = get_back_keyboard()
    else:
        text = "📋 Majburiy kanallar ro'yxati:\n\n"
        for i, channel in enumerate(channels, 1):
            channel_name = channel['channel_username'] if channel['channel_username'] else channel['channel_id']
            text += f"{i}. {channel_name}\n"
        keyboard = get_back_keyboard()
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


# Delete channel - show list
@dp.callback_query(F.data == "admin_delete_channel")
async def callback_delete_channel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    channels = await get_all_channels()
    
    if not channels:
        await callback.answer("❌ O'chirish uchun kanallar yo'q!", show_alert=True)
        return
    
    text = "🗑 O'chirmoqchi bo'lgan kanalni tanlang:"
    keyboard = get_channels_keyboard(channels)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


# Delete channel - confirm
@dp.callback_query(F.data.startswith("delete_channel_"))
async def callback_confirm_delete_channel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    channel_id = callback.data.split("_")[-1]
    channels = await get_all_channels()
    channel = next((c for c in channels if c['id'] == int(channel_id)), None)
    
    if channel:
        await delete_channel(channel['channel_id'])
        await callback.answer("✅ Kanal o'chirildi!", show_alert=True)
    
    # Refresh list
    channels = await get_all_channels()
    if channels:
        text = "🗑 O'chirmoqchi bo'lgan kanalni tanlang:"
        keyboard = get_channels_keyboard(channels)
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        keyboard = get_admin_keyboard()
        await callback.message.edit_text(MESSAGES["admin_panel"], reply_markup=keyboard)


# Add movie - start
@dp.callback_query(F.data == "admin_add_movie")
async def callback_add_movie(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    keyboard = get_cancel_keyboard()
    await callback.message.edit_text(
        "➕ Kino uchun kod kiriting (masalan: KINO001):",
        reply_markup=keyboard
    )
    await state.set_state(AdminStates.waiting_for_movie_code)
    await callback.answer()


# Add movie - receive code
@dp.message(StateFilter(AdminStates.waiting_for_movie_code), F.text)
async def process_movie_code(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    code = message.text.strip().upper()
    await state.update_data(movie_code=code)
    
    keyboard = get_cancel_keyboard()
    await message.answer(
        "📹 Kino faylini yuboring:",
        reply_markup=keyboard
    )
    await state.set_state(AdminStates.waiting_for_movie_file)


# Add movie - receive file
@dp.message(StateFilter(AdminStates.waiting_for_movie_file), F.video | F.document)
async def process_movie_file(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    if message.video:
        file_id = message.video.file_id
    elif message.document:
        file_id = message.document.file_id
    else:
        await message.answer("❌ Iltimos, video fayl yuboring!")
        return
    
    await state.update_data(movie_file_id=file_id)
    
    keyboard = get_cancel_keyboard()
    await message.answer(
        "📝 Kino nomini kiriting:",
        reply_markup=keyboard
    )
    await state.set_state(AdminStates.waiting_for_movie_title)


# Add movie - receive title and save
@dp.message(StateFilter(AdminStates.waiting_for_movie_title), F.text)
async def process_movie_title(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    title = message.text.strip()
    data = await state.get_data()
    
    code = data['movie_code']
    file_id = data['movie_file_id']
    
    success = await add_movie(code, file_id, title, added_by=message.from_user.id)
    
    if success:
        await message.answer(f"✅ Kino muvaffaqiyatli qo'shildi!\nKod: {code}")
    else:
        await message.answer("❌ Bu kod allaqachon mavjud!")
    
    await state.clear()
    keyboard = get_admin_keyboard()
    await message.answer(MESSAGES["admin_panel"], reply_markup=keyboard)


# Delete movie - start
@dp.callback_query(F.data == "admin_delete_movie")
async def callback_delete_movie(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    keyboard = get_cancel_keyboard()
    await callback.message.edit_text(
        "🗑 O'chirmoqchi bo'lgan kino kodini kiriting:",
        reply_markup=keyboard
    )
    await state.set_state(AdminStates.waiting_for_delete_code)
    await callback.answer()


# Delete movie - receive code
@dp.message(StateFilter(AdminStates.waiting_for_delete_code), F.text)
async def process_delete_movie(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    code = message.text.strip().upper()
    movie = await get_movie_by_code(code)
    
    if movie:
        await delete_movie(code)
        await message.answer(f"✅ Kino o'chirildi! (Kod: {code})")
    else:
        await message.answer(MESSAGES["movie_not_found"])
    
    await state.clear()
    keyboard = get_admin_keyboard()
    await message.answer(MESSAGES["admin_panel"], reply_markup=keyboard)


# Broadcast - start
@dp.callback_query(F.data == "admin_broadcast")
async def callback_broadcast(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    keyboard = get_cancel_keyboard()
    await callback.message.edit_text(MESSAGES["broadcast_start"], reply_markup=keyboard)
    await state.set_state(AdminStates.waiting_for_broadcast)
    await callback.answer()


# Broadcast - send message
@dp.message(StateFilter(AdminStates.waiting_for_broadcast))
async def process_broadcast(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    users = await get_all_users()
    success = 0
    failed = 0
    
    await message.answer("📢 Xabar yuborilmoqda...")
    
    for user in users:
        try:
            await bot.copy_message(
                chat_id=user['user_id'],
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            success += 1
            await asyncio.sleep(0.05)  # Avoid hitting rate limits
        except Exception as e:
            failed += 1
            logger.error(f"Failed to send to {user['user_id']}: {e}")
    
    text = MESSAGES["broadcast_success"].format(success=success, failed=failed)
    await message.answer(text)
    
    await state.clear()
    keyboard = get_admin_keyboard()
    await message.answer(MESSAGES["admin_panel"], reply_markup=keyboard)


# Users list
@dp.callback_query(F.data == "admin_users")
async def callback_users(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    users = await get_all_users()
    total = len(users)
    
    text = f"👥 Foydalanuvchilar ro'yxati\n\n"
    text += f"Jami: {total} ta foydalanuvchi\n\n"
    
    # Show first 10 users
    for i, user in enumerate(users[:10], 1):
        username = f"@{user['username']}" if user['username'] else "Username yo'q"
        name = user['first_name'] or "No name"
        text += f"{i}. {name} ({username})\n"
    
    if total > 10:
        text += f"\n... va yana {total - 10} ta foydalanuvchi"
    
    keyboard = get_back_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


# Add admin - start
@dp.callback_query(F.data == "admin_add_admin")
async def callback_add_admin(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    keyboard = get_cancel_keyboard()
    await callback.message.edit_text(
        "👨‍💼 Yangi admin qo'shish\n\nFoydalanuvchini botga /start yuborishini so'rang, keyin uning Telegram ID'sini yuboring.\n\nYoki forward qiling uning xabarini.",
        reply_markup=keyboard
    )
    await state.set_state(AdminStates.waiting_for_admin_id)
    await callback.answer()


# Add admin - receive ID
@dp.message(StateFilter(AdminStates.waiting_for_admin_id), F.text)
async def process_add_admin(message: Message, state: FSMContext):
    if not await is_admin(message.from_user.id):
        await state.clear()
        return
    
    try:
        new_admin_id = int(message.text.strip())
        
        # Check if already admin
        if new_admin_id in ADMIN_IDS or await is_admin_in_db(new_admin_id):
            await message.answer("❌ Bu foydalanuvchi allaqachon admin!")
            await state.clear()
            keyboard = get_admin_keyboard()
            await message.answer(MESSAGES["admin_panel"], reply_markup=keyboard)
            return
        
        # Try to get user info
        try:
            user_info = await bot.get_chat(new_admin_id)
            username = user_info.username if hasattr(user_info, 'username') else None
        except:
            username = None
        
        # Add admin to database
        success = await add_admin(new_admin_id, username, message.from_user.id)
        
        if success:
            await message.answer(f"✅ Yangi admin qo'shildi!\n\nID: {new_admin_id}\nUsername: @{username if username else 'N/A'}")
        else:
            await message.answer("❌ Xatolik yuz berdi!")
        
    except ValueError:
        await message.answer("❌ Noto'g'ri ID! Raqam kiriting.")
    
    await state.clear()
    keyboard = get_admin_keyboard()
    await message.answer(MESSAGES["admin_panel"], reply_markup=keyboard)


# List admins
@dp.callback_query(F.data == "admin_list_admins")
async def callback_list_admins(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    admins = await get_all_admins()
    
    text = "👨‍💼 Adminlar ro'yxati:\n\n"
    text += f"📋 Config adminlar ({len(ADMIN_IDS)} ta):\n"
    for admin_id in ADMIN_IDS:
        text += f"  • ID: {admin_id}\n"
    
    if admins:
        text += f"\n📊 Database adminlar ({len(admins)} ta):\n"
        for admin in admins:
            username = f"@{admin['username']}" if admin['username'] else "N/A"
            text += f"  • {username} (ID: {admin['user_id']})\n"
    
    text += "\n💡 O'chirish uchun quyidan tanlang:"
    
    keyboard = get_admins_keyboard(admins, callback.from_user.id)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


# Delete admin - confirm
@dp.callback_query(F.data.startswith("delete_admin_"))
async def callback_confirm_delete_admin(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        await callback.answer("❌ Sizda admin huquqi yo'q!", show_alert=True)
        return
    
    admin_id = int(callback.data.split("_")[-1])
    
    # Don't allow deleting config admins
    if admin_id in ADMIN_IDS:
        await callback.answer("❌ Config adminni o'chirish mumkin emas!", show_alert=True)
        return
    
    await delete_admin(admin_id)
    await callback.answer("✅ Admin o'chirildi!", show_alert=True)
    
    # Refresh list
    admins = await get_all_admins()
    text = "👨‍💼 Adminlar ro'yxati:\n\n"
    text += f"📋 Config adminlar ({len(ADMIN_IDS)} ta):\n"
    for aid in ADMIN_IDS:
        text += f"  • ID: {aid}\n"
    
    if admins:
        text += f"\n📊 Database adminlar ({len(admins)} ta):\n"
        for admin in admins:
            username = f"@{admin['username']}" if admin['username'] else "N/A"
            text += f"  • {username} (ID: {admin['user_id']})\n"
    
    text += "\n💡 O'chirish uchun quyidan tanlang:"
    
    keyboard = get_admins_keyboard(admins, callback.from_user.id)
    await callback.message.edit_text(text, reply_markup=keyboard)


# Cancel button
@dp.callback_query(F.data == "cancel")
async def callback_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    
    if is_admin(callback.from_user.id):
        keyboard = get_admin_keyboard()
        await callback.message.edit_text(MESSAGES["admin_panel"], reply_markup=keyboard)
    else:
        await callback.message.edit_text(MESSAGES["cancel"])
    
    await callback.answer()


# Close admin panel
@dp.callback_query(F.data == "admin_close")
async def callback_close(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()


# Main function
async def main():
    # Initialize database
    await init_db()
    await init_default_channel()
    logger.info("Database initialized")
    
    # Start polling
    logger.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
