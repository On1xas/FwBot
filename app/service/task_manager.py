import threading
import keyboard
from tkinter import messagebox
from app.service.locale_service import Localization

from app.logging import logger



class TaskManager:
    def __init__(self, app, user_config, locale: Localization):
        self.app = app
        self.user_config = user_config
        self.locale: Localization = locale
        self.task_list = []
        self.stop_event = threading.Event()
        self.stop_func = False
        self.bind_keys()

    def start_task(self, task_func, on_complete_func, name_service):
        self.stop_func = False
        logger.info(f"APP: TASK MANAGER: TASK {name_service} START")
        # Если есть запущенные задачи, прерываем их
        if self.task_list:
            logger.info(f"APP: TASK MANAGER: TASK LIST NOT EMPTY")
            self.interapt_tasks()

        self.stop_event.clear()
        thread = threading.Thread(target=self.run_task, args=(task_func, on_complete_func, name_service))
        thread.start()
        self.task_list.append((thread, name_service))

    def run_task(self, task_func, on_complete_func, name_service):
        try:
            task_func()  # Запускаем задачу
        finally:
            logger.info(f"APP: TASK MANAGER: TASK {name_service} PREPARE TO END")
            on_complete_func()  # Вызываем функцию завершения
            self.task_list.clear()  # Удаляем завершённый поток из списка
            logger.info(f"APP: TASK MANAGER: TASK {name_service} END")

    def interapt_tasks(self):
        logger.info(f"APP: TASK MANAGER: PRESS [F6] INTERAPT BUTTON")
        self.stop_func = True
        logger.info(f"APP: TASK MANAGER: STOP FUNC TRIGGER CHANGED TO {self.stop_func}")

        if self.task_list:
            self.stop_event.set()  # Установка флага остановки
            for thread, name_service in self.task_list:
                thread.join(timeout=1)  # Прерываем поток
            self.task_list.clear()
            messagebox.showinfo(title=self.locale.i10n('task-msgb-si-stoptask-title'), message=self.locale.i10n(message_id='task-msgb-si-stoptask-message', name_service=name_service))
        else:
            messagebox.showinfo(title=self.locale.i10n('task-msgb-si-stoptask-title'), message=self.locale.i10n('task-msgb-si-noprocess-message'))

    def bind_keys(self):
        # Привязываем глобальные клавиши
        keyboard.add_hotkey('f6', self.interapt_tasks)
