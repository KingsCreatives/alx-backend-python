import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    return wrapper

""" your code goes here"""
def retry_on_failure(retries=3, delay=2):
    def decorator(func): 
        @functools.wraps()
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect("users.db")
            for i in range(retries):
                try:
                    return func(*args,**kwargs)
                except sqlite3.Error as e:
                    if i < retries -1:
                        print(f"Database error: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else: 
                        raise
        return wrapper
    return decorator

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Alice')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (2, 'Bob')")
    conn.commit()
    conn.close()

setup_database()


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

try:
    users = fetch_users_with_retry()
    print(users)
except sqlite3.Error as e:
    print(f"Failed to fetch users after multipl retries. Erro : {e}")