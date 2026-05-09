# Базовые действия с таблицами
import sys

sys.path.insert(0, "../dbconnection.py")

from dbconnection import *


class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        return self.dbconn.prefix + "table"

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        return list(self.columns().keys())

    def primary_key(self):
        return ["id"]

    def column_names_without_id(self):
        res = list(self.columns().keys())
        if "id" in res:
            res.remove("id")
        return res

    def table_constraints(self):
        return []

    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name() + " CASCADE"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def insert_one(self, vals):
        # Используем параметризованный запрос для защиты от SQL-инъекций
        columns = self.column_names_without_id()
        placeholders = ", ".join(["%s"] * len(vals))
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(columns) + ") VALUES("
        sql += placeholders + ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, vals)
        self.dbconn.conn.commit()
        return

    def update_one(self, id_value, vals):
        """Обновление записи по id"""
        columns = self.column_names_without_id()
        set_clause = ", ".join([f"{col} = %s" for col in columns])
        sql = f"UPDATE {self.table_name()} SET {set_clause} WHERE {self.primary_key()[0]} = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, vals + [id_value])
        self.dbconn.conn.commit()
        return cur.rowcount

    def delete_one(self, id_value):
        """Удаление записи по id"""
        sql = f"DELETE FROM {self.table_name()} WHERE {self.primary_key()[0]} = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, [id_value])
        self.dbconn.conn.commit()
        return cur.rowcount

    def find_by_id(self, id_value):
        """Поиск записи по id"""
        sql = f"SELECT * FROM {self.table_name()} WHERE {self.primary_key()[0]} = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, [id_value])
        return cur.fetchone()

    def all(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def get_all_with_row_numbers(self):
        """Возвращает список записей с порядковыми номерами"""
        records = self.all()
        return [(i + 1,) + record for i, record in enumerate(records)]

    def print_all(self):
        table = self.all()
        if not table:
            print("Нет записей")
            return
        width = 20
        print(" | ".join(f"{col[:width]:^{width}}" for col in self.column_names()))
        print("-" * (len(self.column_names()) * (width + 3) - 3))
        for line in table:
            print(" | ".join(f"{str(val)[:width]:^{width}}" for val in line))

    def print_with_row_numbers(self):
        """Вывод таблицы с порядковыми номерами строк"""
        records = self.all()
        if not records:
            print("Нет записей")
            return
        col_names = ["№"] + self.column_names()
        width = 15
        print(" | ".join(f"{col[:width]:^{width}}" for col in col_names))
        print("-" * (len(col_names) * (width + 3) - 3))
        for i, record in enumerate(records, 1):
            row = [str(i)] + [str(val) for val in record]
            print(" | ".join(f"{val[:width]:^{width}}" for val in row))
