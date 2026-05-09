from config.settings import Settings
from db.connection import DbConnection
from models.room import RoomsRepository
from models.rack import RacksRepository
from ui.room_ui import RoomUI
from ui.rack_ui import RackUI
from ui.console import clear, menu_loop

def main():
    settings = Settings()
    db = DbConnection(settings)
    room_repo = RoomsRepository(db)
    rack_repo = RacksRepository(db)

    room_ui = RoomUI(room_repo)
    rack_ui = RackUI(rack_repo, room_repo)

    # Проверка: при первом запуске можно создать таблицы (опционально)
    # Но лучше оставить отдельный пункт меню "Инициализация БД"
    # По заданию есть действие "Drop init insert" – его тоже надо реализовать.

    main_options = {
        '1': ("Сброс, инициализация и заполнение тестовыми данными", lambda: init_db(room_repo, rack_repo)),
        '2': ("Работа с помещениями", lambda: room_ui.run()),
        '3': ("Работа со стеллажами", lambda: rack_ui.run()),
    }

    while True:
        clear()
        print("=== Главное меню ===")
        for k, (desc, _) in main_options.items():
            print(f"{k}. {desc}")
        print("0. Выход")
        choice = input("=> ").strip()
        if choice == '0':
            break
        if choice in main_options:
            main_options[choice][1]()
        else:
            print("Неверный выбор. Нажмите Enter.")
            input()

    db.close()

def init_db(room_repo, rack_repo):
    """Сброс, создание и наполнение тестовыми данными"""
    print("Сброс таблиц...")
    rack_repo.drop()
    room_repo.drop()
    print("Создание таблиц...")
    room_repo.create()
    rack_repo.create()
    print("Вставка тестовых данных...")
    # помещения
    rooms_data = [
        ("Склад А", 500, -10, 25, 30, 70),
        ("Цех Б", 1200, 5, 35, 20, 60),
        ("Холодильник В", 300, -25, -10, 50, 90),
    ]
    for data in rooms_data:
        room_repo.insert_one(list(data))
    # стеллажи (подразумеваем, что id помещений начинаются с 1)
    racks_data = [
        (1, 10, 1500), (1, 9, 12000),
        (2, 7, 120), (2, 6, 100),
        (3, 5, 10200), (3, 4, 12),
    ]
    for data in racks_data:
        rack_repo.insert_one(list(data))
    print("Инициализация завершена. Нажмите Enter.")
    input()

if __name__ == "__main__":
    main()
