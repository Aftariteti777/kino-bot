import asyncio
from aiogram import Bot
from config import BOT_TOKEN

async def reset_bot():
    bot = Bot(token=BOT_TOKEN)
    
    # Delete webhook
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Webhook o'chirildi va kutilayotgan update'lar tozalandi")
    
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(reset_bot())
