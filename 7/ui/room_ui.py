from ui.console import (
    clear,
    input_str,
    input_float,
    display_table,
    select_from_list,
    menu_loop,
)
from models.room import RoomsRepository


class RoomUI:
    def __init__(self, repo: RoomsRepository):
        self.repo = repo

    def _get_room_choices(self):
        """Список для select_from_list: (номер, id, описание)"""
        rows = self.repo.all()
        return [(i + 1, row[0], row[1]) for i, row in enumerate(rows)]

    def _collect_room_data(self, current=None):
        """Сбор данных с клавиатуры. current - текущая запись для редактирования (tuple без id)"""
        if current:
            print("Оставьте поле пустым, чтобы не менять.")
            name = input_str(
                f"Название (было: {current[0]}): ", allow_empty=True, max_len=128
            )
            if not name:
                name = current[0]
            volume = input_float(f"Объём (было: {current[1]}): ", min_val=0.001)
            min_temp = input_float(
                f"Мин. температура (было: {current[2]}): ", min_val=-50, max_val=60
            )
            max_temp = input_float(
                f"Макс. температура (было: {current[3]}): ", min_val=-50, max_val=60
            )
            min_humid = input_float(
                f"Мин. влажность (было: {current[4]}): ", min_val=0, max_val=100
            )
            max_humid = input_float(
                f"Макс. влажность (было: {current[5]}): ", min_val=0, max_val=100
            )
        else:
            name = input_str("Название: ", max_len=128)
            volume = input_float("Объём: ", min_val=0.001)
            min_temp = input_float(
                "Мин. температура (-50..60): ", min_val=-50, max_val=60
            )
            max_temp = input_float(
                "Макс. температура (-50..60): ", min_val=-50, max_val=60
            )
            min_humid = input_float("Мин. влажность (0..100): ", min_val=0, max_val=100)
            max_humid = input_float(
                "Макс. влажность (0..100): ", min_val=0, max_val=100
            )

        return [name, volume, min_temp, max_temp, min_humid, max_humid]

    def action_insert(self):
        clear()
        print("--- Добавление помещения ---")
        data = self._collect_room_data()
        validated, err = self.repo.validate_data(data)
        if err:
            print(f"Ошибка: {err}")
            input("Нажмите Enter...")
            return
        self.repo.insert_one(validated)
        print("Помещение добавлено!")
        input("Enter...")

    def action_update(self):
        clear()
        choices = self._get_room_choices()
        room_id = select_from_list(choices, "Выберите помещение для редактирования:")
        if not room_id:
            return
        current = self.repo.find_by_id(room_id)
        if not current:
            print("Помещение не найдено")
            return
        # current = (id, name, volume, min_temp, max_temp, min_humid, max_humid)
        current_data = list(current[1:])  # без id
        new_data = self._collect_room_data(current_data)
        # Если значения не менялись, validated всё равно пройдёт
        validated, err = self.repo.validate_data(new_data)
        if err:
            print(f"Ошибка: {err}")
            input("Enter...")
            return
        self.repo.update_one(room_id, validated)
        print("Помещение обновлено!")
        input("Enter...")

    def action_delete(self):
        clear()
        choices = self._get_room_choices()
        room_id = select_from_list(
            choices, "Выберите помещение для УДАЛЕНИЯ (будут удалены и стеллажи):"
        )
        if not room_id:
            return
        confirm = input(f"Удалить помещение? Введите 'ДА': ").strip().upper()
        if confirm == "ДА":
            self.repo.delete_one(room_id)
            print("Удалено.")
        else:
            print("Отменено.")
        input("Enter...")

    def action_list(self):
        clear()
        rows = self.repo.get_all_for_display()
        columns = ["Название", "Объём", "T min", "T max", "H min", "H max"]
        display_table(columns, rows, row_numbers=True)
        input("Enter...")

    def run(self):
        options = {
            "1": ("Добавить", self.action_insert),
            "2": ("Редактировать", self.action_update),
            "3": ("Удалить", self.action_delete),
            "4": ("Список", self.action_list),
        }
        while True:
            clear()
            print("--- Управление помещениями ---")
            for k, (desc, _) in options.items():
                print(f"{k}. {desc}")
            print("0. Назад")
            choice = input("=> ").strip()
            if choice == "0":
                break
            if choice in options:
                options[choice][1]()
            else:
                print("Неверный выбор. Нажмите Enter.")
                input()
