import aiosqlite
from datetime import datetime
from config import DATABASE_PATH, DEFAULT_CHANNEL_ID


async def init_db():
    """Initialize database with required tables"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Users table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                join_date TEXT,
                last_active TEXT,
                is_active INTEGER DEFAULT 1
            )
        """)
        
        # Movies table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                file_id TEXT NOT NULL,
                title TEXT,
                description TEXT,
                added_by INTEGER,
                added_date TEXT
            )
        """)
        
        # Mandatory channels table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS mandatory_channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT UNIQUE NOT NULL,
                channel_username TEXT,
                added_date TEXT
            )
        """)
        
        # Statistics table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                new_users INTEGER DEFAULT 0,
                movies_sent INTEGER DEFAULT 0
            )
        """)
        
        await db.commit()


async def init_default_channel():
    """Add default mandatory channel if not exists"""
    try:
        await add_channel(DEFAULT_CHANNEL_ID, None)
    except Exception:
        pass  # Channel already exists


# User functions
async def add_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None):
    """Add a new user to the database"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        now = datetime.now().isoformat()
        try:
            await db.execute("""
                INSERT INTO users (user_id, username, first_name, last_name, join_date, last_active)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, username, first_name, last_name, now, now))
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            # User already exists, update last_active
            await db.execute("""
                UPDATE users SET last_active = ? WHERE user_id = ?
            """, (now, user_id))
            await db.commit()
            return False


async def get_all_users():
    """Get all users from database"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_user_count():
    """Get total user count"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def get_active_user_count():
    """Get active user count (last 7 days)"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("""
            SELECT COUNT(*) FROM users 
            WHERE datetime(last_active) > datetime('now', '-7 days')
        """) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


# Movie functions
async def add_movie(code: str, file_id: str, title: str = None, description: str = None, added_by: int = None):
    """Add a new movie to the database"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        now = datetime.now().isoformat()
        try:
            await db.execute("""
                INSERT INTO movies (code, file_id, title, description, added_by, added_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (code.upper(), file_id, title, description, added_by, now))
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def get_movie_by_code(code: str):
    """Get movie by code"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM movies WHERE code = ?", (code.upper(),)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_movie_count():
    """Get total movie count"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM movies") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def delete_movie(code: str):
    """Delete a movie by code"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM movies WHERE code = ?", (code.upper(),))
        await db.commit()


# Channel functions
async def add_channel(channel_id: str, channel_username: str = None):
    """Add a mandatory channel"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        now = datetime.now().isoformat()
        try:
            await db.execute("""
                INSERT INTO mandatory_channels (channel_id, channel_username, added_date)
                VALUES (?, ?, ?)
            """, (channel_id, channel_username, now))
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def get_all_channels():
    """Get all mandatory channels"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM mandatory_channels") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def delete_channel(channel_id: str):
    """Delete a mandatory channel"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM mandatory_channels WHERE channel_id = ?", (channel_id,))
        await db.commit()


async def get_channel_count():
    """Get total channel count"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM mandatory_channels") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0
