from abc import ABC, abstractmethod


class Repository(ABC):
    def __init__(self, db_connection):
        self.dbconn = db_connection

    @abstractmethod
    def table_name(self):
        """Полное имя таблицы с префиксом"""
        pass

    @abstractmethod
    def columns(self):
        """Словарь {колонка: [тип, ...]} для CREATE TABLE"""
        pass

    @abstractmethod
    def primary_key(self):
        """Список колонок первичного ключа (обычно ['id'])"""
        pass

    def table_constraints(self):
        """Дополнительные ограничения (список строк)"""
        return []

    def create(self):
        sql = f"CREATE TABLE {self.table_name()} ("
        col_defs = [f"{k} {' '.join(v)}" for k, v in self.columns().items()]
        all_defs = col_defs + self.table_constraints()
        sql += ", ".join(all_defs) + ")"
        with self.dbconn.conn.cursor() as cur:
            cur.execute(sql)
            self.dbconn.conn.commit()

    def drop(self):
        sql = f"DROP TABLE IF EXISTS {self.table_name()} CASCADE"
        with self.dbconn.conn.cursor() as cur:
            cur.execute(sql)
            self.dbconn.conn.commit()

    def insert_one(self, values):
        cols = self._columns_without_id()
        placeholders = ", ".join(["%s"] * len(values))
        sql = f"INSERT INTO {self.table_name()} ({', '.join(cols)}) VALUES ({placeholders})"
        with self.dbconn.conn.cursor() as cur:
            cur.execute(sql, values)
            self.dbconn.conn.commit()

    def update_one(self, id_value, values):
        cols = self._columns_without_id()
        set_clause = ", ".join([f"{col} = %s" for col in cols])
        pk = self.primary_key()[0]
        sql = f"UPDATE {self.table_name()} SET {set_clause} WHERE {pk} = %s"
        with self.dbconn.conn.cursor() as cur:
            cur.execute(sql, values + [id_value])
            self.dbconn.conn.commit()
            return cur.rowcount

    def delete_one(self, id_value):
        pk = self.primary_key()[0]
        sql = f"DELETE FROM {self.table_name()} WHERE {pk} = %s"
        with self.dbconn.conn.cursor() as cur:
            cur.execute(sql, [id_value])
            self.dbconn.conn.commit()
            return cur.rowcount

    def find_by_id(self, id_value):
        pk = self.primary_key()[0]
        sql = f"SELECT * FROM {self.table_name()} WHERE {pk} = %s"
        with self.dbconn.conn.cursor() as cur:
            cur.execute(sql, [id_value])
            return cur.fetchone()

    def all(self, order_by=None):
        if order_by is None:
            order_by = self.primary_key()
        sql = f"SELECT * FROM {self.table_name()} ORDER BY {', '.join(order_by)}"
        with self.dbconn.conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def _columns_without_id(self):
        cols = list(self.columns().keys())
        if "id" in cols:
            cols.remove("id")
        return cols
