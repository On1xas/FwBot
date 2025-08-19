import json
import os


from typing import List
from app.config.model import User, AllianceConfiguration, GameAccount, Config
from app.logging import logger

from typing import Optional
from pydantic import ValidationError


class ConfigManager:
    def __init__(self, config_path: str):
        self.config_file = config_path
        self.config = self.load_config()

    def initialize_config(self):
        config = Config(
            user=User(
                client_id=0,
                token="",
                expired_time="",
                locale = "ru"
            ),
            alliance_config=AllianceConfiguration(
                count_open_window=0,
                size_window_x=0,
                size_window_y=0,
                path_to_exe="",
                accounts=[]
            ),
            version=""
        )
        logger.info(msg=f"APP: CONFIG_MANAGER: INITIALIZE CONFIG - CONFIG LOADED")
        self.save_config(config)

    def load_config(self) -> Config:
        if os.path.exists(self.config_file):
            logger.info(msg=f"APP: CONFIG_MANAGER: LOAD CONFIG - FILE EXIST")
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    # Пытаемся создать объект Config из загруженных данных
                    config = Config(**data)
                    logger.info(msg=f"APP: CONFIG_MANAGER: LOAD CONFIG - CONFIG LOADED")
                    return config
            except (ValidationError, json.JSONDecodeError) as e:
                # Если данные не соответствуют модели или файл поврежден
                logger.error(msg=f"APP: CONFIG_MANAGER: LOAD CONFIG - INVALID CONFIG FILE: {e}")
                os.remove(self.config_file)  # Удаляем невалидный файл
                logger.info(msg=f"APP: CONFIG_MANAGER: LOAD CONFIG - INVALID FILE REMOVED")
                self.initialize_config()  # Инициализируем новый конфиг
                return self.load_config()  # Загружаем вновь созданную конфигурацию
        else:
            logger.error(msg=f"APP: CONFIG_MANAGER: LOAD CONFIG - FILE NOT EXIST")
            self.initialize_config()  # Инициализация, если файл не существует
            return self.load_config()  # Загружаем вновь созданную конфигурацию

    def save_config(self, config: Config):
        with open(self.config_file, "w") as f:
            json.dump(config.dict(), f, indent=4)
            logger.info(msg=f"APP: CONFIG_MANAGER: SAVE CONFIG - COMPLETED")

    def update_path_exe(self, path: str):
        self.config.alliance_config.path_to_exe = path
        self.save_config(self.config)

    def update_size_window(self, x, y):
        self.config.alliance_config.size_window_x = x
        self.config.alliance_config.size_window_y = y
        self.save_config(self.config)

    def update_count_open_window(self, count: int):
        self.config.alliance_config.count_open_window = count
        self.save_config(self.config)

    def update_alliance_config(self, count_open_window: int, path_to_exe: str, accounts: List[GameAccount]):
        self.config.alliance_config.count_open_window = count_open_window
        self.config.alliance_config.path_to_exe = path_to_exe
        self.config.alliance_config.accounts = accounts
        self.save_config(self.config)

    def update_client_id(self, client_id: int):
        self.config.user.client_id = client_id
        self.save_config(self.config)

    def update_token(self, token: str):
        self.config.user.token = token
        self.save_config(self.config)

    def update_exp_time(self, time: str):
        self.config.user.expired_time = time
        self.save_config(self.config)

    def update_locale(self, locale: str):
        if isinstance(locale, str):
            if locale == "ru" or locale == "en":
                self.config.user.locale = locale
            else:
                self.config.user.locale = "en"
        self.save_config(self.config)