import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.rooms_table import *
from tables.racks_table import *

class Main:
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        self.current_room_id = None      # для помещения, у которого смотрим стеллажи
        self.current_room_record = None

if __name__ == "__main__":
    m = Main()
    m.main_cycle()