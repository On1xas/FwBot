import logging
import logging.config


# Настройка логирования
def setup_logger(log_file_path):

    # logging.basicConfig(

    # Создание логгера
    logger = logging.getLogger(name="APP")
    logger.setLevel(logging.INFO)  # Установка уровня логирования

    root_logger = logging.getLogger()

    # Проверка наличия обработчиков
    if root_logger.hasHandlers():
        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                # Установка уровня логирования
                handler.setLevel(logging.INFO)

                # Установка формата
                formatter = logging.Formatter(
                    'TIME: [%(asctime)s] MSG: %(message)s',
                    datefmt='%H:%M:%S'
                )
                handler.setFormatter(formatter)
                # print(f"Обработчик {handler.__class__.__name__} настроен на уровень {logging.INFO}.")

    # Настройка обработчика для записи в файл
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        'TIME:[%(asctime)s] LEVEL: %(levelname)s   FUNC: %(funcName)s: [%(lineno)d]  MSG: %(message)s',
        datefmt='%Y-%m-%d %H:%M'  # Формат времени до минут
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

#  Настройка обработчика для вывода в консоль (если нужно)
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_formatter = logging.Formatter(
    #     'CONSOLE: [%(asctime)s] - %(levelname)s - %(message)s',
    #     datefmt='%Y-%m-%d %H:%M:%S'
    # )
    # console_handler.setFormatter(console_formatter)
    # logger.addHandler(console_handler)

    logger.info("LOGGER INIT")  # Проверка инициализации логирования
    return logger