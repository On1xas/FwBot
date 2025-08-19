import os
import sys
import logging
import datetime
import glob


def resource_path(relative_path):
    """ Получить абсолютный путь к ресурсу. """
    try:
        base_path = sys._MEIPASS  # Путь к временной директории
    except Exception:
        base_path = os.path.abspath(".")  # Путь в режиме разработки
    logging.info(msg=f"UTILS: RESOURCE PATH: [{os.path.join(base_path, relative_path)}]")
    return os.path.join(base_path, relative_path)

def get_config_path():
    # Определяем путь к конфигурации
    if os.name == 'nt':  # Windows
        config_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'DSClicker')
    else:  # Unix-системы
        config_dir = os.path.join(os.path.expanduser('~'), '.config', 'DSClicker')

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    return os.path.join(config_dir, 'user_config.json')

# def get_logging_path():
#     if os.name == 'nt':  # Windows
#         config_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'DSClicker', 'log')
#     else:  # Unix-системы
#         config_dir = os.path.join(os.path.expanduser('~'), '.config', 'DSClicker')

#     if not os.path.exists(config_dir):
#         os.makedirs(config_dir)

#     log_file_path = os.path.join(config_dir, 'log_file.log')

#     # Создаем файл, если он не существует
#     if not os.path.exists(log_file_path):
#         with open(log_file_path, 'w') as log_file:
#             log_file.write('')  # Создаем пустой файл

#     logging.info(msg="Log File init")
#     return log_file_path

def get_logging_path():
    if os.name == 'nt':  # Windows
        config_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'DSClicker', 'log')
    else:  # Unix-системы
        config_dir = os.path.join(os.path.expanduser('~'), '.config', 'DSClicker')

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # Форматируем имя файла с текущей датой
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file_path = os.path.join(config_dir, f'logs_{today_date}.log')

    # Удаление логов старше 10 дней
    delete_old_logs(config_dir)

    logging.info("Log File initialized")
    return log_file_path

def delete_old_logs(config_dir):
    # Получаем текущую дату
    now = datetime.datetime.now()
    # Ищем все лог-файлы в директории
    log_files = glob.glob(os.path.join(config_dir, 'logs_*.log'))

    for log_file in log_files:
        # Получаем дату из имени файла
        file_date_str = os.path.basename(log_file)[5:15]  # 'logs_YYYY-MM-DD.log'
        file_date = datetime.datetime.strptime(file_date_str, '%Y-%m-%d')

        # Если файл старше 10 дней, удаляем его
        if (now - file_date).days > 10:
            os.remove(log_file)
            logging.info(f"Deleted old log file: {log_file}")