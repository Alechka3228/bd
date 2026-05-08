import sys

sys.path.append("tables")

from project_config import *
from dbconnection import *
from tables.rooms_table import *
from tables.racks_table import *
from help import *


class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        rooms_table = RoomsTable()
        racks_table = RacksTable()
        rooms_table.create()
        racks_table.create()
        return

    def db_insert_somethings(self):
        rooms_table = RoomsTable()
        rooms_table.insert_one(["Склад1", 65, 18, 26, 30, 70])
        rooms_table.insert_one(["Склад2", 45, 16, 24, 40, 60])
        rooms_table.insert_one(["Склад3", 30, 15, 28, 20, 80])

        racks_table = RacksTable()
        racks_table.insert_one([1, 10, 500])
        racks_table.insert_one([1, 15, 750])
        racks_table.insert_one([1, 20, 1000])
        racks_table.insert_one([2, 8, 400])
        racks_table.insert_one([2, 12, 600])
        racks_table.insert_one([2, 18, 900])
        racks_table.insert_one([3, 10, 500])
        racks_table.insert_one([3, 10, 500])
        racks_table.insert_one(["3", 25, 1200])

    def db_drop(self):
        rooms_table = RoomsTable()
        racks_table = RacksTable()
        racks_table.drop()
        rooms_table.drop()
        return
    
    def show_menu(self, points):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): """
        for i in points:
            menu += "\n" + i[0] + " " # что жмать
            menu += i[1] + ";" # что делать будет 
        print(menu)
        return

    @check_done
    def drop_init_with_somethings(self):
        self.db_drop()
        self.db_init()
        self.db_insert_somethings()

    @check_done
    def manipulations_with_rooms(self):
        self.show_menu(room_manipulation_menu)
        choice = input("=> ").strip()
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        else:
            print_that_user_is_disabled("Такого варианта нет")

    @check_done
    def manipulations_with_racks(self):
        self.show_menu(room_manipulation_menu)
        choice = input("=> ").strip()
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        else:
            print_that_user_is_disabled("Такого варианта нет")

    def read_next_step(self):
        return safety_input("=> ").strip()

    def main_cycle(self):
        self.show_menu(main_menu)
        current_menu = self.read_next_step()

        while current_menu != "q":
            if current_menu == "1":
                self.drop_init_with_somethings()
            elif current_menu == "2":
                self.manipulations_with_rooms()
            elif current_menu == "3":
                pass
            elif current_menu == "4":
                pass
            elif current_menu == "5":
                pass
            elif current_menu == "6":
                pass
            else:
                print_that_user_is_disabled("Такого варианта нет")

            self.show_menu(main_menu)
            current_menu = self.read_next_step()

        # q
        print("До свидания!")
        return

    def test(self):
        DbTable.dbconn.test()


m = Main()
m.main_cycle()
