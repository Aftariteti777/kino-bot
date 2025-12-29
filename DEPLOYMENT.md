# Railway Deployment Guide

## Railway.app'ga Deploy Qilish

### 1. Railway Account Yaratish
1. [Railway.app](https://railway.app) ga o'ting
2. GitHub orqali sign up qiling
3. Email tasdiqlang

### 2. GitHub Repository Yaratish
1. [GitHub.com](https://github.com) da yangi repository yarating
2. Repository nomini kiriting: `kino-bot`
3. **Private** tanlang (bot tokenini himoya qilish uchun)

### 3. Kodlarni GitHub'ga yuklash

```bash
# Git init qiling
git init
git add .
git commit -m "Initial commit"

# GitHub repository'ga ulaning
git remote add origin https://github.com/YOUR_USERNAME/kino-bot.git
git branch -M main
git push -u origin main
```

### 4. Railway'ga Deploy

1. Railway.app'ga kiring
2. **"New Project"** tugmasini bosing
3. **"Deploy from GitHub repo"** ni tanlang
4. **kino-bot** repository'ni tanlang
5. **"Deploy Now"** ni bosing

### 5. Environment Variables Qo'shish

Railway dashboardda:
1. Proyektingizni oching
2. **"Variables"** tabga o'ting
3. Quyidagi variablelarni qo'shing:

```
BOT_TOKEN=8505783569:AAFq_r5RKdju3FabZ44S_pVH4yYLcN7gvBU
ADMIN_IDS=889845009
DATABASE_PATH=bot_database.db
```

4. **"Deploy"** tugmasini bosing

### 6. Bot Ishga Tushishi

Railway avtomatik deploy qiladi. Loglarni ko'rish uchun:
- **"Deployments"** tabga o'ting
- Loglarni real-time kuzating

✅ **Bot tayyor!** Railway'da 24/7 ishlaydi!

---

## Render.com'ga Deploy (Alternativ)

### 1. Render Account
1. [Render.com](https://render.com) ga o'ting
2. GitHub orqali sign up

### 2. New Web Service
1. Dashboard'da **"New +"** → **"Web Service"**
2. GitHub repository'ni ulang
3. Sozlamalar:
   - **Name**: kino-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free

### 3. Environment Variables
- BOT_TOKEN
- ADMIN_IDS
- DATABASE_PATH

### 4. Deploy
**"Create Web Service"** ni bosing

⚠️ **Eslatma**: Render'ning bepul planida 15 daqiqadan keyin bot "sleep" ga o'tadi.

---

## VPS'ga Deploy (Professional)

### 1. VPS Sotib Olish
- [Vultr](https://vultr.com) - $3.5/oy
- [DigitalOcean](https://digitalocean.com) - $4/oy

### 2. Ubuntu Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv git -y

# Clone project
git clone https://github.com/YOUR_USERNAME/kino-bot.git
cd kino-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
# Paste your configuration and save (Ctrl+X, Y, Enter)

# Test bot
python main.py
```

### 3. Systemd Service (Bot Doimiy Ishlashi)

```bash
# Create service file
sudo nano /etc/systemd/system/kino-bot.service
```

Paste this:
```ini
[Unit]
Description=Kino Telegram Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/kino-bot
Environment="PATH=/home/YOUR_USERNAME/kino-bot/venv/bin"
ExecStart=/home/YOUR_USERNAME/kino-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable kino-bot
sudo systemctl start kino-bot

# Check status
sudo systemctl status kino-bot

# View logs
sudo journalctl -u kino-bot -f
```

---

## Qaysi Birini Tanlash?

| Server | Narx | Uptime | Tavsiya |
|--------|------|--------|---------|
| **Railway.app** | $5 kredit/oy | 24/7 | ⭐⭐⭐⭐⭐ Eng yaxshi! |
| **Render.com** | Bepul | Sleep 15min | ⭐⭐⭐ Test uchun |
| **VPS** | $3.5-5/oy | 24/7 | ⭐⭐⭐⭐⭐ Professional |
| **PythonAnywhere** | Bepul | 24/7 | ⭐⭐ Juda cheklangan |

---

## Troubleshooting

### Bot ishlamayapti
```bash
# Logs ko'rish (Railway)
railway logs

# Logs ko'rish (VPS)
sudo journalctl -u kino-bot -f
```

### Database yo'qoldi
- Railway/Render'da database fayllarni saqlash uchun **Volume** qo'shing
- Yoki **PostgreSQL** database ishlatishni o'ylang

### Bot qayta-qayta restart bo'lyapti
- Logs'ni tekshiring
- Environment variables to'g'ri ekanligini tekshiring

---

## Keyingi Qadamlar

1. ✅ Bot serverga joylashtirish
2. 📊 PostgreSQL database qo'shish (Railway bepul beradi)
3. 🔔 Error monitoring qo'shish
4. 📈 Analytics qo'shish
5. 🎨 Botni yaxshilash

Omad!
