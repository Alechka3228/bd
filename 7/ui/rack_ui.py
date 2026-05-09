from ui.console import (
    clear,
    input_int,
    input_float,
    display_table,
    select_from_list,
    menu_loop,
)
from models.rack import RacksRepository
from models.room import RoomsRepository


class RackUI:
    def __init__(self, rack_repo: RacksRepository, room_repo: RoomsRepository):
        self.rack_repo = rack_repo
        self.room_repo = room_repo

    def _get_room_choices(self):
        rows = self.room_repo.all()
        return [(i + 1, row[0], row[1]) for i, row in enumerate(rows)]

    def _get_rack_choices_for_room(self, room_id):
        racks = self.rack_repo.find_by_room(room_id)
        return [
            (i + 1, rack[0], f"Вместимость {rack[2]}, макс. вес {rack[3]}")
            for i, rack in enumerate(racks)
        ]

    def action_list_by_room(self):
        clear()
        choices = self._get_room_choices()
        room_id = select_from_list(
            choices, "Выберите помещение для просмотра стеллажей:"
        )
        if not room_id:
            return
        racks = self.rack_repo.find_by_room(room_id)
        if not racks:
            print("В этом помещении нет стеллажей.")
        else:
            columns = ["ID стеллажа", "Вместимость", "Макс. вес"]
            rows = [(r[0], r[2], r[3]) for r in racks]
            display_table(columns, rows, row_numbers=True)
        input("Enter...")

    def action_add(self):
        clear()
        choices = self._get_room_choices()
        room_id = select_from_list(
            choices, "Выберите помещение для добавления стеллажа:"
        )
        if not room_id:
            return
        print("--- Добавление стеллажа ---")
        capacity = input_int("Вместимость (целое >0): ", min_val=1)
        max_weight = input_float("Максимальный вес (>0): ", min_val=0.001)
        err = self.rack_repo.validate_rack_data(room_id, capacity, max_weight)
        if err:
            print(f"Ошибка: {err}")
        else:
            self.rack_repo.insert_one([room_id, capacity, max_weight])
            print("Стеллаж добавлен.")
        input("Enter...")

    def action_delete(self):
        clear()
        room_choices = self._get_room_choices()
        room_id = select_from_list(
            room_choices, "Выберите помещение, в котором удалить стеллаж:"
        )
        if not room_id:
            return
        rack_choices = self._get_rack_choices_for_room(room_id)
        if not rack_choices:
            print("В этом помещении нет стеллажей.")
            input("Enter...")
            return
        rack_id = select_from_list(rack_choices, "Выберите стеллаж для удаления:")
        if not rack_id:
            return
        confirm = input("Удалить стеллаж? Введите 'ДА': ").strip().upper()
        if confirm == "ДА":
            self.rack_repo.delete_one(rack_id)
            print("Удалено.")
        else:
            print("Отменено.")
        input("Enter...")

    def run(self):
        options = {
            "1": ("Показать стеллажи в помещении", self.action_list_by_room),
            "2": ("Добавить стеллаж в помещение", self.action_add),
            "3": ("Удалить стеллаж", self.action_delete),
        }
        while True:
            clear()
            print("--- Управление стеллажами ---")
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
