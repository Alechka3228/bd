from db.repository import Repository
from utils.validators import (
    validate_room_name,
    validate_volume,
    validate_temperature,
    validate_humidity,
    validate_temp_range,
    validate_humid_range,
)


class RoomsRepository(Repository):
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

    def get_all_for_display(self):
        """Возвращает список всех записей для отображения (без id в UI)"""
        rows = self.all()
        return [
            (row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows
        ]

    def validate_data(self, data, is_update=False):
        """
        data: список значений в порядке колонок без id: [name, volume, min_temp, max_temp, min_humid, max_humid]
        возвращает кортеж (очищенные_данные, сообщение_об_ошибке)
        """
        if len(data) != 6:
            return None, f"Ожидается 6 полей, получено {len(data)}"

        name = str(data[0]).strip()
        err = validate_room_name(name)
        if err:
            return None, err

        try:
            volume = float(data[1])
            err = validate_volume(volume)
            if err:
                return None, err
        except ValueError:
            return None, "Объём должен быть числом"

        try:
            min_temp = float(data[2])
            max_temp = float(data[3])
            err = validate_temperature(min_temp, "min_temp")
            if err:
                return None, err
            err = validate_temperature(max_temp, "max_temp")
            if err:
                return None, err
            err = validate_temp_range(min_temp, max_temp)
            if err:
                return None, err
        except ValueError:
            return None, "Температура должна быть числом"

        try:
            min_humid = float(data[4])
            max_humid = float(data[5])
            err = validate_humidity(min_humid, "min_humid")
            if err:
                return None, err
            err = validate_humidity(max_humid, "max_humid")
            if err:
                return None, err
            err = validate_humid_range(min_humid, max_humid)
            if err:
                return None, err
        except ValueError:
            return None, "Влажность должна быть числом"

        validated = [name, volume, min_temp, max_temp, min_humid, max_humid]
        return validated, None
