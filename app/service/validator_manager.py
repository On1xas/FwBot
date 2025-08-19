import requests
import uuid
from tkinter import messagebox
from datetime import datetime, timedelta, timezone

from app.service.task_manager import TaskManager
from app.logging import logger
from app.config.config_manager import ConfigManager
from app.service.locale_service import Localization

class ValidatorManager():
    def __init__(self, app, config, task_manager):
        self.app = app
        self.locale: Localization = self.app.locale
        self.config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.server_url = "http://45.144.64.228:5000"
        # self.server_url = "http://127.0.0.1:5000"
        self.server_status = False
        self.online = 0
        self.last_connection = ""
        self.temp_status_code = 0
        self.failed_sync_time = 0


    def get_hwID(self):
        # Получаем уникальный идентификатор устройства
        hw_id = str(uuid.getnode())
        return hw_id


    def auth(self):
        logger.info('APP: VALIDATOR MANAGER: AUTH IN ACTION')
        url = f"{self.server_url}/api/v1/auth"

        payload = {
            "client_id": self.config.config.user.client_id,
            "token": self.config.config.user.token,
            "hwID": self.get_hwID()
        }

        try:
            response = requests.post(url, json=payload)
            self.temp_status_code = response.status_code
            response.raise_for_status()  # Вызывает исключение для статусов 4xx и 5xx
            if response.status_code == 200 and self.config.config.user.token == "" and self.config.config.user.client_id == 0:
                return {
                "error": "",
                "status": "Firstly"}
            # Обработка успешного ответа
            resp = response.json()
            self.online = resp.get('online', False)
            self.last_connection = resp.get('time', None)
            self.server_status = True
            # self.app.user_frame.update_server_status()
            logger.info('APP: VALIDATOR MANAGER: CONNECTION TO SERVER - GOOD')
            resp['status_code'] = response.status_code
            if self.check_time_sync(server_time_str=resp['time']):
                return resp
            else:
                return {
                "error": "Дата и время устройства не соответвует реальному",
                "status": "Fail",
                "status_code": self.temp_status_code}


        except requests.exceptions.ConnectionError as http_err:
            logger.error(f'APP: VALIDATOR MANAGER: HTTP error occurred: {http_err}')
            self.handle_connection_error(http_err)
            return {
                "error": "Connection Error",
                "status": "Fail",
                "status_code": self.temp_status_code}

        except Exception as e:
            self.server_status = False
            self.online = 0
            self.app.user_frame.update_server_status()
            logger.error(f'APP: VALIDATOR MANAGER: CONNECTION ERROR: {e}')
            return {
                "error": "Connection Error",
                "status": "Fail",
                "status_code": self.temp_status_code}

    def handle_connection_error(self, response):
        self.server_status = False
        self.online = 0
        self.app.user_frame.update_server_status()
        logger.info('APP: VALIDATOR MANAGER: SERVER CONNECTION ERROR')

    def days_until(self, date_str):
        if date_str == "":
            return self.locale.i10n('day_until_not_active')
        # Определяем формат входной даты
        date_format = "%Y-%m-%d %H:%M"  # Пример: "2025-02-09 12:00"

        # Преобразуем строку в объект datetime с учетом часового пояса UTC
        target_date = datetime.strptime(date_str, date_format).replace(tzinfo=timezone.utc)

        if self.last_connection == "":
            current_date = datetime.now(timezone.utc)
        else:
            current_date = datetime.strptime(self.last_connection, date_format).replace(tzinfo=timezone.utc)


        # Проверяем, истекла ли дата
        if target_date < current_date:
            return self.locale.i10n('day_until_expired')

        # Вычисляем количество дней до целевой даты
        delta = (target_date - current_date).days

        # Определяем склонение
        if delta % 10 == 1 and delta % 100 != 11:
            declension = self.locale.i10n('day_until_day')
        elif 2 <= delta % 10 <= 4 and not (12 <= delta % 100 <= 14):
            declension = self.locale.i10n('day_until_days2')
        else:
            declension = self.locale.i10n('day_until_days')

        # Формируем и возвращаем результат
        return f"{target_date.strftime('%d.%m.%Y')}({delta} {declension})"

    def get_time(self):
        # Определяем формат входной даты
        date_format = "%Y-%m-%d %H:%M"  # Пример: "2025-02-09 12:00"
         # Определяем формат входной даты
        try:
            # Преобразуем строку в объект datetime с учетом часового пояса UTC
            target_date = datetime.strptime(self.last_connection, date_format).replace(tzinfo=timezone.utc)
            current_date = datetime.now(timezone.utc)

            # Вычисляем разницу во времени
            time_difference = current_date - target_date

            # Проверяем, если разница составляет 60 минут
            if abs(time_difference) <= timedelta(minutes=15):
                logger.info(f'APP: VALIDATOR MANAGER: TIME IS GOOD')
                return
                # Здесь можно добавить дополнительную логику проверки
            else:
                url = f"{self.server_url}/api/v1/get_time"  # Убедитесь, что URL соответствует вашему приложению
                payload = {
                    "client_id": int(self.config.config.user.client_id)
                }

                try:
                    response = requests.get(url, params=payload)
                    response.raise_for_status()
                    logger.info(f'APP: VALIDATOR MANAGER: GET TIME FROM SERVER')
                    resp = response.json()
                    self.online = resp['online']
                    self.last_connection = resp['time']
                    self.server_status = True
                    self.app.user_frame.update_server_status()
                    self.config.update_exp_time(time=resp['exp_time'])

                except requests.exceptions.HTTPError as http_err:
                    logger.error(f'APP: VALIDATOR MANAGER: HTTP error occurred: {http_err}')
                    if self.failed_sync_time > 1:
                        logger.error(f'APP: VALIDATOR MANAGER: ERROR CONNECTION. STOP TASK')
                        self.handle_error()
                        messagebox.showerror(title="SERVER STATUS ERROR", message="Сервер временно недоступен, обратитесь к администратору")
                        return
                    else:
                        self.failed_sync_time += 1
                        logger.error('APP: VALIDATOR MANAGER: ERROR CONNECTION. FAILED COUNT: [%s]', self.failed_sync_time)
                        return

                except Exception as e:
                    logger.error(f'APP: VALIDATOR MANAGER: ERROR CONNECTION TO THE SERVER, TIME NOT SYNC')
                    if self.failed_sync_time > 1:
                        logger.error(f'APP: VALIDATOR MANAGER: ERROR CONNECTION. STOP TASK')
                        self.handle_error()
                        messagebox.showerror(title="SERVER STATUS ERROR", message="Сервер временно недоступен, обратитесь к администратору")
                        return
                    else:
                        self.failed_sync_time += 1
                        logger.error('APP: VALIDATOR MANAGER: ERROR CONNECTION. FAILED COUNT: [%s]', self.failed_sync_time)
                        return

        except ValueError:
            logger.info(f'APP: VALIDATOR MANAGER: Неверный формат даты.')


        target_date = datetime.strptime(self.config.config.user.expired_time, date_format).replace(tzinfo=timezone.utc)
        current_date = datetime.strptime(self.last_connection, date_format).replace(tzinfo=timezone.utc)

        # Проверяем, истекла ли дата
        if target_date < current_date:
            self.task_manager.stop_event.set()
            self.task_manager.stop_func = True
            self.app.validate = False
            self.failed_sync_time = 0
            self.app.user_frame.update_license_status()
            self.app.user_frame.update_server_status()

            self.app.render(self.app.render_license_frame)
            logger.info(f'APP: VALIDATOR MANAGER: LICENSE TIME END')
            messagebox.showerror(title="License STATUS ERROR", message="Срок действия лицензии истёк, обратитесь к администратору")
        else:
            self.failed_sync_time = 0
            logger.info(f'APP: VALIDATOR MANAGER: LICENSE EXPIRATION TIME IS GOOD')

    def handle_error(self, response=None):
        self.server_status = False
        self.task_manager.stop_event.set()
        self.task_manager.stop_func = True
        self.failed_sync_time = 0
        self.app.validate = False
        self.app.user_frame.update_server_status()
        self.app.user_frame.update_license_status()
        self.app.render(self.app.render_license_frame)
        logger.info(f'APP: VALIDATOR MANAGER: HANDLE ERROR COMPLITE')


    def check_time_sync(self, server_time_str):
    # Получаем текущее время на ПК в UTC
        local_time = datetime.now(timezone.utc)

        # Преобразуем серверное время из строки в объект datetime
        try:
            server_time = datetime.strptime(server_time_str, "%Y-%m-%d %H:%M")
            # Преобразуем серверное время в UTC
            server_time = server_time.replace(tzinfo=timezone.utc)
        except ValueError:
            logger.info(f'APP: VALIDATOR MANAGER: ERROR Value - SERVER TIME INCORRECT')
            return False

        # Сравниваем время
        time_difference = abs((local_time - server_time).total_seconds())
        result = time_difference < 4 * 3600
        if result:
            logger.info(f'APP: VALIDATOR MANAGER: SYNC SERVER TIME DONE')
            return True
        logger.info(f'APP: VALIDATOR MANAGER: SYNC SERVER TIME DONT SYNC. ')
        return False