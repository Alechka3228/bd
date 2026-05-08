# Таблица Помещения и особые действия с ней.

from dbtable import *

class RoomsTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "rooms"

    def columns(self):
        return {"room_name": ["varchar(128)", "NOT NULL"],
                "volume": ["numeric", "NOT NULL DEFAULT 1"],
                "min_temp": ["numeric", "NOT NULL DEFAULT -30"],
                "max_temp": ["numeric", "NOT NULL DEFAULT 30"],
                "min_humid": ["numeric", "NOT NULL DEFAULT 0"],
                "max_humid": ["numeric", "NOT NULL DEFAULT 100"]}
    
    def primary_key(self):
        return ['id']    

    def table_constraints(self):
        return ["PRIMARY KEY(id)",
                "CONSTRAINT chk_room_volume_positive CHECK (volume > 0)",
                "CONSTRAINT chk_room_temp_range CHECK (min_temp <= max_temp)",
                "CONSTRAINT chk_room_humid_range CHECK (min_humid <= max_humid)",
                "CONSTRAINT chk_room_temp_bounds CHECK (min_temp >= -50 AND max_temp <= 60)",
                "CONSTRAINT chk_room_humid_bounds CHECK (min_humid >= 0 AND max_humid <= 100)"]

    def all_by_room_name(self, name):
        """Получить все помещения по имени (частичное совпадение)"""
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE room_name LIKE %s"
        sql += " ORDER BY room_name"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, ('%' + name + '%',))
        return cur.fetchall()

    def get_by_temp_range(self, min_temp, max_temp):
        """Получить помещения, подходящие по температурному диапазону"""
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE min_temp <= %s AND max_temp >= %s"
        sql += " ORDER BY id"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (min_temp, max_temp))
        return cur.fetchall()