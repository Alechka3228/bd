# Таблица Стеллажи и особые действия с ней.

from dbtable import *

class RacksTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "racks"

    def columns(self):
        return {"room_id": ["integer", "NOT NULL"],
                "capacity": ["integer", "NOT NULL"],
                "max_weight": ["numeric", "NOT NULL"],
                "client_id": ["integer", None]}
    
    def primary_key(self):
        return ['id']    

    def table_constraints(self):
        return ["PRIMARY KEY(id)",
                "CONSTRAINT chk_rack_capacity_positive CHECK (capacity > 0)",
                "CONSTRAINT chk_rack_max_weight_positive CHECK (max_weight > 0)",
                "FOREIGN KEY (room_id) REFERENCES rooms(id) ON UPDATE CASCADE ON DELETE CASCADE"]

    def all_by_room_id(self, room_id):
        """Получить все стеллажи в указанном помещении"""
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE room_id = %s"
        sql += " ORDER BY id"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (str(room_id),))
        return cur.fetchall()