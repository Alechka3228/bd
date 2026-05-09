from dbconnection import DbConnection
from help import check_done, display_menu, main_menu, print_no_option, table_menu
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
        display_menu("Rooms menu", table_menu)
        choice = input("=> ")
        if choice == "1":
            table.manual_insert()
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            table.print_all()
        elif choice == "0":
            print("Go back")
            return
        else:
            print_no_option()

    @check_done
    def racks_menu(self):
        table = RacksTable()
        display_menu("Racks menu", table_menu)
        choice = input("=> ")
        if choice == "1":
            table.manual_insert()
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            table.print_all()
        elif choice == "0":
            print("Go back")
            return
        else:
            print_no_option()

    def main_cycle(self):
        while True:
            display_menu("Main menu", main_menu)
            choice = input("=> ")
            if choice == "1":
                self.drop_init_insert()
            elif choice == "2":
                self.rooms_menu()
            elif choice == "3":
                self.racks_menu()
            elif choice == "0":
                print("Bye")
                return
            else:
                print_no_option()


if __name__ == "__main__":
    m = Main()
    m.main_cycle()
