# Таблица Стеллажи и особые действия с ней.

from dbtable import *

class RacksTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "racks"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "room_id": ["integer", "NOT NULL"],
                "capacity": ["integer", "NOT NULL"],
                "max_weight": ["numeric", "NOT NULL"]}
    
    def primary_key(self):
        return ['id']    

    def table_constraints(self):
        return ["PRIMARY KEY(id)",
                "CONSTRAINT chk_rack_capacity_positive CHECK (capacity > 0)",
                "CONSTRAINT chk_rack_max_weight_positive CHECK (max_weight > 0)",
                "FOREIGN KEY (room_id) REFERENCES rooms(id) ON UPDATE CASCADE ON DELETE CASCADE"]