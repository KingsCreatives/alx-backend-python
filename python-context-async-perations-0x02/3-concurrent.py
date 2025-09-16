import sqlite3
import aiosqlite
import asyncio

DB = "my.db"

async def async_fetch_users(db_path):
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


async def async_fetch_older_users(db_path):
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        async with db.execute("SELECT * FROM users WHERE age > ? ", (40,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

async def fetch_concurrently():
    task1 = asyncio.create_task(async_fetch_users(DB))
    task2 = asyncio.create_task(async_fetch_older_users(DB))
    all_users, older_users = await asyncio.gather(task1, task2)
    print("All users:", all_users)
    print("Older users:", older_users)

asyncio.run(fetch_concurrently())