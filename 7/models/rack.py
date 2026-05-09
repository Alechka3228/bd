from db.repository import Repository
from utils.validators import validate_positive_int, validate_positive_number


class RacksRepository(Repository):
    def table_name(self):
        return self.dbconn.prefix + "racks"

    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "room_id": ["integer", "NOT NULL"],
            "capacity": ["integer", "NOT NULL"],
            "max_weight": ["numeric", "NOT NULL"],
        }

    def primary_key(self):
        return ["id"]

    def table_constraints(self):
        return [
            "CONSTRAINT chk_rack_capacity_positive CHECK (capacity > 0)",
            "CONSTRAINT chk_rack_max_weight_positive CHECK (max_weight > 0)",
            "FOREIGN KEY (room_id) REFERENCES rooms(id) ON UPDATE CASCADE ON DELETE CASCADE",
        ]

    def find_by_room(self, room_id):
        sql = f"SELECT * FROM {self.table_name()} WHERE room_id = %s ORDER BY id"
        with self.dbconn.conn.cursor() as cur:
            cur.execute(sql, [room_id])
            return cur.fetchall()

    def validate_rack_data(self, room_id, capacity, max_weight):
        if not isinstance(room_id, int) or room_id <= 0:
            return "Неверный идентификатор помещения"
        err = validate_positive_int(capacity, "Вместимость")
        if err:
            return err
        err = validate_positive_number(max_weight, "Максимальный вес")
        if err:
            return err
        return None  # ОК
