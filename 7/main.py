import sys

sys.path.append("tables")

from project_config import *
from dbconnection import *
from tables.rooms_table import *
from tables.racks_table import *


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
        rooms_table.insert_one(["Test", "Test", "Test"])
        rooms_table.insert_one(["Test2", "Test2", "Test2"])
        rooms_table.insert_one(["Test3", "Test3", "Test3"])

        racks_table = RacksTable()
        racks_table.insert_one([1, "123"])
        racks_table.insert_one([2, "123"])
        racks_table.insert_one([3, "123"])

    def db_drop(self):
        rooms_table = RoomsTable()
        racks_table = RacksTable()
        racks_table.drop()
        rooms_table.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while current_menu != "9":
            if current_menu == "0":
                next_step = self.read_next_step()
            elif current_menu == "1":
                next_step = self.read_next_step()
            elif current_menu == "2":
                next_step = self.read_next_step()
        print("До свидания!")
        return

    def test(self):
        DbTable.dbconn.test()


m = Main()
m.main_cycle()
