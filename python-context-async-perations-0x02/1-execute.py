import sqlite3

class ExecuteQuery:
    def __init__(self,query, db_path, params=(25,)):
        self.db_path = db_path
        self.query = query
        self.params = params
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.cur.execute(self.query, self.params)
        self.result = self.cur.fetchall()
        return self.result
    
    def __exit__(self,exc_type,exc,tb):
        if hasattr(self, "conn"):
            self.conn.close()
        return False


with ExecuteQuery("SELECT * FROM users WHERE age > ?", "test_users.db", (25,)) as results:
    for row in results:
        print(dict(row))


    
