import time
import sqlite3 
import functools


query_cache = {}

"""your code goes here"""
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

def cache_query(func):
    @functools.wraps()
    def wrapper(*args,**kwargs):
        query = kwargs.get('query')
        if(query in query_cache):
            return query_cache[query]
        else:
            result = func(*args,**kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    time.sleep(1)
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

### First call
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)


#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")