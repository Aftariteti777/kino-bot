# 🎬 Kino Bot

Telegram bot for sharing movies with mandatory channel subscription and admin panel.

## Xususiyatlar (Features)

- ✅ Kino kod orqali yuborish (Send movies by code)
- ✅ Majburiy kanal a'zolik tekshiruvi (Force channel subscription)
- ✅ Admin panel (Admin panel)
- ✅ Kanallarni boshqarish (Channel management)
- ✅ Statistika (Statistics)
- ✅ Barcha foydalanuvchilarga xabar yuborish (Broadcast messages)
- ✅ Kino qo'shish va o'chirish (Add and delete movies)

## O'rnatish (Installation)

### 1. Python o'rnatilganligini tekshiring (Check Python installation)
```powershell
python --version
```

### 2. Loyihani clone qiling yoki yuklab oling

### 3. Virtual environment yarating (Create virtual environment)
```powershell
python -m venv venv
```

### 4. Virtual environment'ni faollashtiring (Activate virtual environment)
```powershell
.\venv\Scripts\Activate.ps1
```

Agar xatolik bo'lsa (If error occurs):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 5. Kerakli kutubxonalarni o'rnating (Install dependencies)
```powershell
pip install -r requirements.txt
```

### 6. .env faylini yarating (Create .env file)
`.env.example` faylidan nusxa oling va `.env` nomini bering:
```powershell
Copy-Item .env.example .env
```

### 7. .env faylini sozlang (Configure .env file)
`.env` faylini ochib quyidagi ma'lumotlarni kiriting:

```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
DATABASE_PATH=bot_database.db
```

- `BOT_TOKEN`: [@BotFather](https://t.me/botfather) dan olingan bot token
- `ADMIN_IDS`: Admin foydalanuvchilarning Telegram ID'lari (vergul bilan ajratilgan)

### 8. Botni ishga tushiring (Run the bot)
```powershell
python main.py
```

## Foydalanish (Usage)

### Oddiy foydalanuvchilar uchun (For regular users):
1. Botni ishga tushiring: `/start`
2. Kerakli kanallarga a'zo bo'ling
3. Kino kodini yuboring (masalan: `KINO001`)
4. Bot sizga kinoni yuboradi

### Admin uchun (For admins):

#### Admin panelni ochish:
```
/admin
```

#### Admin panel imkoniyatlari:

**📊 Statistika**
- Jami foydalanuvchilar soni
- Faol foydalanuvchilar (oxirgi 7 kun)
- Jami kinolar soni
- Majburiy kanallar soni

**➕ Kanal qo'shish**
1. "Kanal qo'shish" tugmasini bosing
2. Kanal username (@mychannel) yoki ID (-1001234567890) kiriting

**📋 Kanallar ro'yxati**
- Barcha majburiy kanallarni ko'ring

**🗑 Kanal o'chirish**
- Ro'yxatdan kanalni tanlang va o'chiring

**➕ Kino qo'shish**
1. "Kino qo'shish" tugmasini bosing
2. Kino kodni kiriting (masalan: KINO001)
3. Kino faylini yuboring
4. Kino nomini kiriting

**🗑 Kino o'chirish**
- Kino kodini kiriting va o'chiring

**📢 Xabar yuborish**
- Barcha foydalanuvchilarga xabar yuboring (broadcast)

**👥 Foydalanuvchilar**
- Foydalanuvchilar ro'yxatini ko'ring

## Ma'lumotlar bazasi tuzilishi (Database Structure)

### users jadval (users table)
- user_id
- username
- first_name
- last_name
- join_date
- last_active
- is_active

### movies jadval (movies table)
- id
- code
- file_id
- title
- description
- added_by
- added_date

### mandatory_channels jadval (mandatory_channels table)
- id
- channel_id
- channel_username
- added_date

### statistics jadval (statistics table)
- id
- date
- new_users
- movies_sent

## Telegram ID ni aniqlash (Find your Telegram ID)

1. [@userinfobot](https://t.me/userinfobot) botiga yozing
2. `/start` buyrug'ini yuboring
3. Bot sizga ID ni yuboradi

yoki

1. [@raw_data_bot](https://t.me/raw_data_bot) botiga yozing
2. ID ni `message.from.id` dan topasiz

## Kanal ID ni aniqlash (Find Channel ID)

1. Kanalingizga [@raw_data_bot](https://t.me/raw_data_bot) ni admin qiling
2. Kanalga xabar yuboring
3. Bot sizga kanal ID ni ko'rsatadi

yoki

1. Kanal username ishlatilsa (@mychannel), uni to'g'ridan-to'g'ri kiriting

## Xavfsizlik (Security)

- `.env` faylini hech qachon Git'ga yuklamang
- Admin ID'larni ehtiyotkorlik bilan saqlang
- Bot tokenni hech kimga bermang

## Xatolarni hal qilish (Troubleshooting)

### Bot ishlamayapti (Bot not working)
- `.env` faylda token to'g'ri kiritilganligini tekshiring
- Internet aloqangizni tekshiring
- Bot foydalanuvchilarning xabarlarini qabul qilish huquqiga ega ekanligini tekshiring

### Majburiy kanal ishlamayapti (Force subscription not working)
- Botni kanalga admin sifatida qo'shganligingizni tekshiring
- Bot "a'zolarni ko'rish" huquqiga ega bo'lishi kerak

### Xabar yuborish ishlamayapti (Broadcast not working)
- Bot foydalanuvchilarga xabar yuborish huquqiga ega ekanligini tekshiring
- Rate limit xatoligi uchun kutish vaqtini oshiring

## Muallif (Author)

Created for Uzbek cinema community

## Litsenziya (License)

MIT License

## Qo'shimcha ma'lumot (Additional Information)

Agar yordam kerak bo'lsa yoki xatolik topsangiz, murojaat qiling.

---

**Eslatma:** Bu bot faqat ta'lim maqsadida yaratilgan. Mualliflik huquqlariga rioya qiling.
