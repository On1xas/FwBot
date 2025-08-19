from app.config.config_manager import ConfigManager
from app.utils.resourse_path import resource_path, get_config_path
from app.service.locale_service import Localization

config_path = get_config_path()
config = ConfigManager(config_path)
locale = Localization(locale=config.config.user.locale)
