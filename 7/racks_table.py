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

    def get_racks_by_room(self, room_id):
        """Получить все стеллажи для указанного помещения"""
        sql = f"SELECT * FROM {self.table_name()} WHERE room_id = %s ORDER BY id"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, [room_id])
        return cur.fetchall()

    def print_racks_by_room(self, room_id, room_name):
        """Вывести стеллажи для конкретного помещения"""
        racks = self.get_racks_by_room(room_id)
        if not racks:
            print(f"В помещении '{room_name}' нет стеллажей")
            return False

        print(f"\n--- Стеллажи в помещении '{room_name}' ---")
        print(f"{'№':<4} {'ID':<6} {'Вместимость':<12} {'Макс. вес':<12}")
        print("-" * 40)
        for i, rack in enumerate(racks, 1):
            print(f"{i:<4} {rack[0]:<6} {rack[2]:<12} {rack[3]:<12}")
        return True

    def get_rack_choices_by_room(self, room_id):
        """Возвращает список стеллажей для выбора (номер, id, вместимость, вес)"""
        racks = self.get_racks_by_room(room_id)
        return [(i + 1, rack[0], rack[2], rack[3]) for i, rack in enumerate(racks)]

    def select_rack_by_user(self, room_id, prompt="Выберите стеллаж"):
        """Позволяет пользователю выбрать стеллаж по номеру строки"""
        choices = self.get_rack_choices_by_room(room_id)
        if not choices:
            print("Нет доступных стеллажей")
            return None
        print(f"\n{prompt}:")
        for num, rack_id, capacity, weight in choices:
            print(f"  {num}. Вместимость: {capacity}, Макс. вес: {weight}")
        try:
            choice = int(safety_input("=> Номер: "))
            for num, rack_id, capacity, weight in choices:
                if num == choice:
                    return rack_id
            print("Неверный выбор")
            return None
        except ValueError:
            print("Введите число")
            return None

    def manual_insert_with_room(self, room_id):
        """Добавление стеллажа для указанного помещения"""
        print(f"\n--- Добавление стеллажа в помещение ID={room_id} ---")

        try:
            capacity_input = safety_input("Вместимость (целое число > 0): ")
            capacity = int(capacity_input)
            if capacity <= 0:
                raise ValueError(f"capacity должно быть > 0, получено {capacity}")
        except (ValueError, TypeError):
            raise TypeError(f"capacity должно быть целым числом > 0")

        try:
            max_weight_input = safety_input("Максимальный вес (> 0): ")
            max_weight = float(max_weight_input)
            if max_weight <= 0:
                raise ValueError(f"max_weight должно быть > 0, получено {max_weight}")
        except (ValueError, TypeError):
            raise TypeError(f"max_weight должно быть числом > 0")

        vals = [room_id, capacity, max_weight]
        self.insert_one(vals)
        print("Стеллаж успешно добавлен!")

    def manual_delete_by_room(self, room_id):
        """Удаление стеллажа в указанном помещении"""
        print(f"\n--- Удаление стеллажа ---")
        choices = self.get_rack_choices_by_room(room_id)
        if not choices:
            print("В этом помещении нет стеллажей для удаления")
            return

        print("Выберите стеллаж для удаления:")
        for num, rack_id, capacity, weight in choices:
            print(f"  {num}. Вместимость: {capacity}, Макс. вес: {weight}")

        try:
            choice = int(safety_input("=> Номер: "))
            rack_id = None
            for num, rid, cap, wgt in choices:
                if num == choice:
                    rack_id = rid
                    break
            if rack_id is None:
                print("Неверный выбор")
                return

            confirm = safety_input(
                f"Удалить стеллаж (вместимость {cap}, вес {wgt})? (да/нет): "
            )
            if confirm.lower() != "да":
                print("Удаление отменено")
                return

            self.delete_one(rack_id)
            print("Стеллаж успешно удалён!")
        except ValueError:
            print("Введите число")
