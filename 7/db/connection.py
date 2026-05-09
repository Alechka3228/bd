import psycopg2


class DbConnection:
    def __init__(self, settings):
        self.conn = psycopg2.connect(
            dbname=settings.dbname,
            user=settings.user,
            password=settings.password,
            host=settings.host,
        )
        self.prefix = settings.dbtableprefix

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()

    def __del__(self):
        self.close()

    def test(self):
        # можно оставить для проверки, но обычно не нужно
        pass
