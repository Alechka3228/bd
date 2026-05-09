from .dbtable import *


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

    # def column_names(self):
    #     return [
    #         "id",
    #         "room_name",
    #         "volume",
    #         "min_temp",
    #         "max_temp",
    #         "min_humid",
    #         "max_humid",
    #     ]

    # def column_names_without_id(self):
    #     return ["room_name", "volume", "min_temp", "max_temp", "min_humid", "max_humid"]

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
