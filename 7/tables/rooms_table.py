# Таблица Помещения и особые действия с ней.

from dbtable import *

class RoomsTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "rooms"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "room_name": ["varchar(128)", "NOT NULL"],
                "volume": ["numeric", "NOT NULL DEFAULT 1"],
                "min_temp": ["numeric", "NOT NULL DEFAULT -30"],
                "max_temp": ["numeric", "NOT NULL DEFAULT 30"],
                "min_humid": ["numeric", "NOT NULL DEFAULT 0"],
                "max_humid": ["numeric", "NOT NULL DEFAULT 100"]}
    
    def column_names(self):
        return ["id",
                "room_name",
                "volume",
                "min_temp",
                "max_temp",
                "min_humid",
                "max_humid"]
    
    def column_names_without_id(self):
        return ["room_name",
                "volume",
                "min_temp",
                "max_temp",
                "min_humid",
                "max_humid"]
    
    def primary_key(self):
        return ['id']    

    def table_constraints(self):
        return ["CONSTRAINT chk_room_volume_positive CHECK (volume > 0)",
                "CONSTRAINT chk_room_temp_range CHECK (min_temp <= max_temp)",
                "CONSTRAINT chk_room_humid_range CHECK (min_humid <= max_humid)",
                "CONSTRAINT chk_room_temp_bounds CHECK (min_temp >= -50 AND max_temp <= 60)",
                "CONSTRAINT chk_room_humid_bounds CHECK (min_humid >= 0 AND max_humid <= 100)"]
    
    def insert_one(self, vals):
        # Проверяем, что передано ровно 6 значений (все столбцы, кроме id)
        if len(vals) != 6:
            raise ValueError(f"Ожидалось 6 значений, получено {len(vals)}")
        
        # Проверка типов для каждого столбца
        # room_name: varchar(128) — должна быть строка
        if not isinstance(vals[0], str):
            raise TypeError(f"room_name должна быть строкой, получен {type(vals[0]).__name__}")
        elif len(vals[0]) > 128:
            raise ValueError(f"room_name превышает 128 символов: {len(vals[0])}")
        
        # volume: числовое — должно быть int или float
        elif not isinstance(vals[1], (int, float)):
            raise TypeError(f"volume должно быть числом, получен {type(vals[1]).__name__}")
        elif vals[1] <= 0:
            raise ValueError(f"volume должно быть > 0, получено {vals[1]}")
        
        # min_temp: числовое — должно быть int или float
        elif not isinstance(vals[2], (int, float)):
            raise TypeError(f"min_temp должно быть числом, получен {type(vals[2]).__name__}")
        elif vals[2] < -50:
            raise ValueError(f"min_temp не может быть меньше -50, получено {vals[2]}")
        
        # max_temp: числовое — должно быть int или float
        elif not isinstance(vals[3], (int, float)):
            raise TypeError(f"max_temp должно быть числом, получен {type(vals[3]).__name__}")
        elif vals[3] > 60:
            raise ValueError(f"max_temp не может превышать 60, получено {vals[3]}")
        elif vals[2] > vals[3]:
            raise ValueError(f"min_temp ({vals[2]}) не может быть больше max_temp ({vals[3]})")
        
        # min_humid: числовое — должно быть int или float
        elif not isinstance(vals[4], (int, float)):
            raise TypeError(f"min_humid должно быть числом, получен {type(vals[4]).__name__}")
        elif vals[4] < 0:
            raise ValueError(f"min_humid не может быть меньше 0, получено {vals[4]}")
        
        # max_humid: числовое — должно быть int или float
        elif not isinstance(vals[5], (int, float)):
            raise TypeError(f"max_humid должно быть числом, получен {type(vals[5]).__name__}")
        elif vals[5] > 100:
            raise ValueError(f"max_humid не может превышать 100, получено {vals[5]}")
        elif vals[4] > vals[5]:
            raise ValueError(f"min_humid ({vals[4]}) не может быть больше max_humid ({vals[5]})")
        
        # Если все проверки пройдены, форматируем значения для SQL
        for i in range(0, len(vals)):
            if type(vals[i]) == str:
                vals[i] = "'" + vals[i] + "'"   # оборачиваем строки в кавычки
            else:
                vals[i] = str(vals[i])           # числа преобразуем в строку
        
        # Формируем SQL-запрос
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        sql += ", ".join(vals) + ")"
        
        # Выполняем запрос
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return