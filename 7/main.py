from dbconnection import DbConnection
from help import check_done, display_menu, main_menu, print_no_option, table_menu, safety_input
from project_config import ProjectConfig
from dbtable import DbTable
from racks_table import RacksTable
from rooms_table import RoomsTable


class Main:
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection

    def room_init(self):
        rooms_table = RoomsTable()
        rooms_table.create()

    def racks_init(self):
        racks_table = RacksTable()
        racks_table.create()

    def rooms_drop(self):
        rooms_table = RoomsTable()
        rooms_table.drop()

    def racks_drop(self):
        racks_table = RacksTable()
        racks_table.drop()

    def db_drop(self):
        self.rooms_drop()
        self.racks_drop()

    def db_init(self):
        self.room_init()
        self.racks_init()

    def db_insert_smth(self):
        rooms_table = RoomsTable()
        rooms_table.insert_one(["Склад А", 500, -10, 25, 30, 70])
        rooms_table.insert_one(["Цех Б", 1200, 5, 35, 20, 60])
        rooms_table.insert_one(["Холодильник В", 300, -25, -10, 50, 90])

        racks_table = RacksTable()
        racks_table.insert_one([1, 10, 1500])
        racks_table.insert_one([1, 9, 12000])
        racks_table.insert_one([2, 7, 120])
        racks_table.insert_one([2, 6, 100])
        racks_table.insert_one([3, 5, 10200])
        racks_table.insert_one([3, 4, 12])

    @check_done
    def drop_init_insert(self):
        self.db_drop()
        self.db_init()
        self.db_insert_smth()

    @check_done
    def rooms_menu(self):
        table = RoomsTable()
        # Расширенное меню для помещений
        rooms_menu_options = {
            1: "Добавить помещение",
            2: "Редактировать помещение",
            3: "Удалить помещение",
            4: "Показать все помещения",
            0: "Назад"
        }
        while True:
            display_menu("Помещения", rooms_menu_options)
            choice = safety_input("=> ")
            if choice == "1":
                try:
                    table.manual_insert()
                except Exception as e:
                    print(f"Ошибка: {e}")
            elif choice == "2":
                try:
                    table.manual_update()
                except Exception as e:
                    print(f"Ошибка: {e}")
            elif choice == "3":
                try:
                    table.manual_delete()
                except Exception as e:
                    print(f"Ошибка: {e}")
            elif choice == "4":
                table.print_with_row_numbers()
            elif choice == "0":
                print("Возврат в главное меню")
                return
            else:
                print_no_option()

    @check_done
    def racks_menu(self):
        rooms_table = RoomsTable()
        racks_table = RacksTable()
        
        # Расширенное меню для стеллажей
        racks_menu_options = {
            1: "Показать стеллажи в помещении",
            2: "Добавить стеллаж в помещение",
            3: "Удалить стеллаж",
            0: "Назад"
        }
        
        while True:
            display_menu("Стеллажи", racks_menu_options)
            choice = safety_input("=> ")
            
            if choice == "1":
                # Просмотр стеллажей по помещению
                room_id = rooms_table.select_room_by_user("Выберите помещение для просмотра стеллажей")
                if room_id:
                    room = rooms_table.find_by_id(room_id)
                    if room:
                        racks_table.print_racks_by_room(room_id, room[1])
                    else:
                        print("Помещение не найдено")
            
            elif choice == "2":
                # Добавление стеллажа с ключом помещения
                room_id = rooms_table.select_room_by_user("Выберите помещение для добавления стеллажа")
                if room_id:
                    try:
                        racks_table.manual_insert_with_room(room_id)
                    except Exception as e:
                        print(f"Ошибка: {e}")
            
            elif choice == "3":
                # Удаление стеллажа в выбранном помещении
                room_id = rooms_table.select_room_by_user("Выберите помещение, в котором нужно удалить стеллаж")
                if room_id:
                    try:
                        racks_table.manual_delete_by_room(room_id)
                    except Exception as e:
                        print(f"Ошибка: {e}")
            
            elif choice == "0":
                print("Возврат в главное меню")
                return
            else:
                print_no_option()

    def main_cycle(self):
        while True:
            display_menu("Главное меню", main_menu)
            choice = safety_input("=> ")
            if choice == "1":
                self.drop_init_insert()
            elif choice == "2":
                self.rooms_menu()
            elif choice == "3":
                self.racks_menu()
            elif choice == "0":
                print("До свидания!")
                return
            else:
                print_no_option()


if __name__ == "__main__":
    m = Main()
    m.main_cycle()
