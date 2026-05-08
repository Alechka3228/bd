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
    
    def column_names(self):
        return ["id",
                "room_id",
                "capacity",
                "max_weight"]
    
    def column_names_without_id(self):
        return ["room_id",
                "capacity",
                "max_weight"]
    
    
    def primary_key(self):
        return ['id']    

    def table_constraints(self):
        return ["CONSTRAINT chk_rack_capacity_positive CHECK (capacity > 0)",
                "CONSTRAINT chk_rack_max_weight_positive CHECK (max_weight > 0)",
                "FOREIGN KEY (room_id) REFERENCES rooms(id) ON UPDATE CASCADE ON DELETE CASCADE"]
    
    def insert_one(self, vals):
        # Проверяем, что передано ровно 3 значения (все столбцы, кроме ID)
        if len(vals) != 3:
            raise ValueError(f"Ожидается 3 значения (room_id, capacity, max_weight), получено {len(vals)}")
        
        # Проверка типа для каждого столбца
        # room_id: целое число - должен быть int
        if not isinstance(vals[0], int):
            raise TypeError(f"room_id должно быть целым числом, получено {type(vals[0]).__name__}")
        elif vals[0] <= 0:
            raise ValueError(f"room_id должно быть положительным, получено {vals[0]}")
        
        # capacity: целое число - должен быть int
        elif not isinstance(vals[1], int):
            raise TypeError(f"capacity должно быть целым числом, получено {type(vals[1]).__name__}")
        elif vals[1] <= 0:
            raise ValueError(f"capacity должно быть > 0, получено {vals[1]}")
        
        # max_weight: число - должен быть int или float
        elif not isinstance(vals[2], (int, float)):
            raise TypeError(f"max_weight должно быть числом, получено {type(vals[2]).__name__}")
        elif vals[2] <= 0:
            raise ValueError(f"max_weight должно быть > 0, получено {vals[2]}")
        
        # Если все проверки пройдены, форматируем значения для SQL
        for i in range(0, len(vals)):
            if type(vals[i]) == str:
                vals[i] = "'" + vals[i] + "'"
            else:
                vals[i] = str(vals[i])
        
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        sql += ", ".join(vals) + ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return