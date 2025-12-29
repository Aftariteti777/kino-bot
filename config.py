import os
from dotenv import load_dotenv

load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(admin_id) for admin_id in os.getenv("ADMIN_IDS", "").split(",") if admin_id]

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot_database.db")

# Default mandatory channel (will be added automatically)
DEFAULT_CHANNEL_ID = "-1003426188280"  # Your main channel ID

# Messages
MESSAGES = {
    "start": "🎬 Assalomu alaykum! Kino bot'ga xush kelibsiz!\n\n"
             "Kino kodini yuboring va men sizga kinoni jo'nataman.\n\n"
             "Misol: KINO001",
    
    "not_subscribed": "⚠️ Botdan foydalanish uchun quyidagi kanallarga a'zo bo'lishingiz kerak:\n\n",
    
    "subscribed": "✅ Rahmat! Endi botdan foydalanishingiz mumkin.",
    
    "movie_not_found": "❌ Kino topilmadi. Iltimos, to'g'ri kodni kiriting.",
    
    "movie_sent": "✅ Kino jo'natildi!",
    
    "admin_panel": "👨‍💼 Admin panel\n\nQuyidagi bo'limlardan birini tanlang:",
    
    "statistics": "📊 Statistika:\n\n"
                  "👥 Jami foydalanuvchilar: {total_users}\n"
                  "🟢 Faol foydalanuvchilar: {active_users}\n"
                  "🎬 Jami kinolar: {total_movies}\n"
                  "📢 Majburiy kanallar: {total_channels}",
    
    "broadcast_start": "📢 Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:",
    
    "broadcast_success": "✅ Xabar {success} ta foydalanuvchiga yuborildi!\n"
                         "❌ {failed} ta foydalanuvchiga yuborilmadi.",
    
    "channel_add": "➕ Kanal username yoki ID'sini kiriting:\n\n"
                   "Misol: @mychannel yoki -1001234567890",
    
    "channel_added": "✅ Kanal muvaffaqiyatli qo'shildi!",
    
    "channel_removed": "✅ Kanal o'chirildi!",
    
    "cancel": "❌ Bekor qilindi.",
}
