import sqlite3

class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        if hasattr(self, "conn"):
            self.conn.close()
        return False


with DatabaseConnection("my.db") as conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    for row in rows:
        print(dict(row))
