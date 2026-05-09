from dbtable import DbTable
from help import safety_input


class RoomsTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "rooms"

    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "room_name": ["varchar(128)", "NOT NULL"],
            "volume": ["numeric", "NOT NULL DEFAULT 1"],
            "min_temp": ["numeric", "NOT NULL DEFAULT -30"],
            "max_temp": ["numeric", "NOT NULL DEFAULT 30"],
            "min_humid": ["numeric", "NOT NULL DEFAULT 0"],
            "max_humid": ["numeric", "NOT NULL DEFAULT 100"],
        }

    def primary_key(self):
        return ["id"]

    def table_constraints(self):
        return [
            "CONSTRAINT chk_room_volume_positive CHECK (volume > 0)",
            "CONSTRAINT chk_room_temp_range CHECK (min_temp <= max_temp)",
            "CONSTRAINT chk_room_humid_range CHECK (min_humid <= max_humid)",
            "CONSTRAINT chk_room_temp_bounds CHECK (min_temp >= -50 AND max_temp <= 60)",
            "CONSTRAINT chk_room_humid_bounds CHECK (min_humid >= 0 AND max_humid <= 100)",
        ]

    def manual_insert(self):
        vals = []
        for number, column in enumerate(self.column_names_without_id()):
            print(f"{number + 1}. {column}")
            vals.append(safety_input("=> "))

        if len(vals) != 6:
            raise ValueError(f"Ожидается 6 значений, получено {len(vals)}")

        try:
            room_name = str(vals[0])
            if len(room_name) > 128:
                raise ValueError(f"room_name превышает 128 символов: {len(room_name)}")
        except (ValueError, TypeError) as e:
            raise TypeError(
                f"room_name должна быть строкой, получен {type(vals[0]).__name__}"
            ) from e

        try:
            volume = float(vals[1])
            if volume <= 0:
                raise ValueError(f"volume должно быть > 0, получено {volume}")
        except (ValueError, TypeError):
            raise TypeError(
                f"volume должно быть числом, получен {type(vals[1]).__name__}"
            )

        try:
            min_temp = float(vals[2])
            if min_temp < -50:
                raise ValueError(
                    f"min_temp не может быть меньше -50, получено {min_temp}"
                )
        except (ValueError, TypeError):
            raise TypeError(
                f"min_temp должно быть числом, получен {type(vals[2]).__name__}"
            )

        try:
            max_temp = float(vals[3])
            if max_temp > 60:
                raise ValueError(f"max_temp не может превышать 60, получено {max_temp}")
            if min_temp > max_temp:
                raise ValueError(
                    f"min_temp ({min_temp}) не может быть больше max_temp ({max_temp})"
                )
        except (ValueError, TypeError):
            raise TypeError(
                f"max_temp должно быть числом, получен {type(vals[3]).__name__}"
            )

        try:
            min_humid = float(vals[4])
            if min_humid < 0:
                raise ValueError(
                    f"min_humid не может быть меньше 0, получено {min_humid}"
                )
        except (ValueError, TypeError):
            raise TypeError(
                f"min_humid должно быть числом, получен {type(vals[4]).__name__}"
            )

        try:
            max_humid = float(vals[5])
            if max_humid > 100:
                raise ValueError(
                    f"max_humid не может превышать 100, получено {max_humid}"
                )
            if min_humid > max_humid:
                raise ValueError(
                    f"min_humid ({min_humid}) не может быть больше max_humid ({max_humid})"
                )
        except (ValueError, TypeError):
            raise TypeError(
                f"max_humid должно быть числом, получен {type(vals[5]).__name__}"
            )

        vals = [
            str(vals[0]),
            float(vals[1]),
            float(vals[2]),
            float(vals[3]),
            float(vals[4]),
            float(vals[5]),
        ]
        self.insert_one(vals)
