from dbtable import DbTable
from help import safety_input


class RacksTable(DbTable):
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

    def manual_insert(self):
        vals = []
        for number, column in enumerate(self.column_names_without_id()):
            print(f"{number + 1}. {column}")
            vals.append(safety_input("=>"))

        if len(vals) != 3:
            raise ValueError(
                f"Ожидается 3 значения (room_id, capacity, max_weight), получено {len(vals)}"
            )

        try:
            room_id = int(vals[0])
            if room_id <= 0:
                raise ValueError(
                    f"room_id должно быть положительным, получено {room_id}"
                )
        except (ValueError, TypeError):
            raise TypeError(
                f"room_id должно быть целым числом, получено {type(vals[0]).__name__}"
            )

        try:
            capacity = int(vals[1])
            if capacity <= 0:
                raise ValueError(f"capacity должно быть > 0, получено {capacity}")
        except (ValueError, TypeError):
            raise TypeError(
                f"capacity должно быть целым числом, получено {type(vals[1]).__name__}"
            )

        try:
            max_weight = float(vals[2])
            if max_weight <= 0:
                raise ValueError(f"max_weight должно быть > 0, получено {max_weight}")
        except (ValueError, TypeError):
            raise TypeError(
                f"max_weight должно быть числом, получено {type(vals[2]).__name__}"
            )

        vals = [int(vals[0]), int(vals[1]), float(vals[2])]
        self.insert_one(vals)
