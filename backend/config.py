import json
import os
from typing import Any

class Config:
    _instance = None

    def __new__(cls, *args, **kwargs) -> Any:
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        with open(self.config_path, 'r') as config_file:
            config = json.load(config_file)
            self.database = config["database"]
            self.file_paths = config["file_paths"]

    @property
    def database_url(self) -> str:
        db = self.database
        return f'postgresql://{db["username"]}:{db["password"]}@{db["host"]}:{db["port"]}/{db["database_name"]}'

    def update_config(self, key: str, value: Any) -> None:
        config = {

            "database": self.database,
            "file_paths": self.file_paths
        }
        keys = key.split('.')
        d = config
        for k in keys[:-1]:
            d = d[k]
        d[keys[-1]] = value
        with open(self.config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
        self._load_config()  # Reload the updated config
