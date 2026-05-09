import yaml


class Settings:
    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
            self.dbname = cfg["dbname"]
            self.user = cfg["user"]
            self.password = cfg["password"]
            self.host = cfg["host"]
            self.dbtableprefix = cfg["dbtableprefix"]
