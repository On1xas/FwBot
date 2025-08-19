from app.utils.resourse_path import get_logging_path
from app.logging.log_config import setup_logger


log_file_path = get_logging_path()
logger = setup_logger(log_file_path)