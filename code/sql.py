import sqlite3


class SQL:
    def __init__(self):
        self.conn = sqlite3.connect("../data/Base.dbs")
        self.cursor = self.conn.cursor()

    def select_all(self, table):
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_where(self, table, column, value):
        query = f"SELECT * FROM {table} WHERE {column}='{value}'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_npc_name(id):
        return SQL().select_where("npc", "dataname", id)[0][1]

    def close(self):
        self.conn.close()
