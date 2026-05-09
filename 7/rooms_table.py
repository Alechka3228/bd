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

    def get_room_choices(self):
        """Возвращает список помещений для выбора (номер_строки, id, имя)"""
        records = self.all()
        return [(i + 1, record[0], record[1]) for i, record in enumerate(records)]

    def select_room_by_user(self, prompt="Выберите помещение"):
        """Позволяет пользователю выбрать помещение по номеру строки"""
        choices = self.get_room_choices()
        if not choices:
            print("Нет доступных помещений")
            return None
        print(f"\n{prompt}:")
        for num, room_id, name in choices:
            print(f"  {num}. {name}")
        try:
            choice = int(safety_input("=> Номер: "))
            for num, room_id, name in choices:
                if num == choice:
                    return room_id
            print("Неверный выбор")
            return None
        except ValueError:
            print("Введите число")
            return None

    def manual_insert(self):
        vals = []
        print("\n--- Добавление нового помещения ---")
        for number, column in enumerate(self.column_names_without_id()):
            print(f"{number + 1}. {column}")
            vals.append(safety_input("=> "))

        if len(vals) != 6:
            raise ValueError(f"Ожидается 6 значений, получено {len(vals)}")

        # Валидация
        room_name = str(vals[0])
        if len(room_name) > 128:
            raise ValueError(f"room_name превышает 128 символов: {len(room_name)}")

        volume = float(vals[1])
        if volume <= 0:
            raise ValueError(f"volume должно быть > 0, получено {volume}")

        min_temp = float(vals[2])
        if min_temp < -50:
            raise ValueError(f"min_temp не может быть меньше -50, получено {min_temp}")

        max_temp = float(vals[3])
        if max_temp > 60:
            raise ValueError(f"max_temp не может превышать 60, получено {max_temp}")
        if min_temp > max_temp:
            raise ValueError(f"min_temp ({min_temp}) не может быть больше max_temp ({max_temp})")

        min_humid = float(vals[4])
        if min_humid < 0:
            raise ValueError(f"min_humid не может быть меньше 0, получено {min_humid}")

        max_humid = float(vals[5])
        if max_humid > 100:
            raise ValueError(f"max_humid не может превышать 100, получено {max_humid}")
        if min_humid > max_humid:
            raise ValueError(f"min_humid ({min_humid}) не может быть больше max_humid ({max_humid})")

        vals = [room_name, volume, min_temp, max_temp, min_humid, max_humid]
        self.insert_one(vals)
        print("Помещение успешно добавлено!")

    def manual_update(self):
        """Редактирование помещения"""
        print("\n--- Редактирование помещения ---")
        room_id = self.select_room_by_user("Выберите помещение для редактирования")
        if room_id is None:
            return

        # Получаем текущие данные
        current = self.find_by_id(room_id)
        if not current:
            print("Помещение не найдено")
            return

        col_names = self.column_names_without_id()
        current_values = list(current[1:])  # пропускаем id

        print("\nТекущие значения (оставьте поле пустым, чтобы не менять):")
        new_vals = []
        for i, (col, cur_val) in enumerate(zip(col_names, current_values)):
            print(f"{i + 1}. {col} (текущее: {cur_val})")
            user_input = safety_input("=> Новое значение (Enter для пропуска): ")
            if user_input.strip() == "":
                new_vals.append(cur_val)
            else:
                new_vals.append(user_input)

        # Валидация
        room_name = str(new_vals[0])
        if len(room_name) > 128:
            raise ValueError(f"room_name превышает 128 символов: {len(room_name)}")

        volume = float(new_vals[1])
        if volume <= 0:
            raise ValueError(f"volume должно быть > 0, получено {volume}")

        min_temp = float(new_vals[2])
        if min_temp < -50:
            raise ValueError(f"min_temp не может быть меньше -50, получено {min_temp}")

        max_temp = float(new_vals[3])
        if max_temp > 60:
            raise ValueError(f"max_temp не может превышать 60, получено {max_temp}")
        if min_temp > max_temp:
            raise ValueError(f"min_temp ({min_temp}) не может быть больше max_temp ({max_temp})")

        min_humid = float(new_vals[4])
        if min_humid < 0:
            raise ValueError(f"min_humid не может быть меньше 0, получено {min_humid}")

        max_humid = float(new_vals[5])
        if max_humid > 100:
            raise ValueError(f"max_humid не может превышать 100, получено {max_humid}")
        if min_humid > max_humid:
            raise ValueError(f"min_humid ({min_humid}) не может быть больше max_humid ({max_humid})")

        new_vals = [float(x) if i > 0 else x for i, x in enumerate(new_vals)]
        new_vals[0] = str(new_vals[0])

        self.update_one(room_id, new_vals)
        print("Помещение успешно обновлено!")

    def manual_delete(self):
        """Удаление помещения с каскадным удалением связанных стеллажей"""
        print("\n--- Удаление помещения ---")
        print("ВНИМАНИЕ! При удалении помещения будут удалены все стеллажи в нём!")
        
        room_id = self.select_room_by_user("Выберите помещение для удаления")
        if room_id is None:
            return

        # Получаем имя помещения для подтверждения
        current = self.find_by_id(room_id)
        if not current:
            print("Помещение не найдено")
            return

        print(f"\nВы уверены, что хотите удалить помещение '{current[1]}'?")
        confirm = safety_input("Введите 'ДА' для подтверждения: ")
        if confirm.upper() != "ДА":
            print("Удаление отменено")
            return

        self.delete_one(room_id)
        print("Помещение успешно удалено!")
