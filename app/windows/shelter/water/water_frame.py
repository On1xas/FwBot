import time
from tkinter import ttk
import tkinter as tk
from tkinter import SOLID, messagebox

from pygetwindow import PyGetWindowException
from app.utils.resourse_path import resource_path
from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager
from app.service.game_object_service_OLD import GameObjectService
from app.service.locale_service import Localization
from app.service.window_manager import WindowManager, Window
from app.logging import logger


class ShelterWaterFrame(ttk.Frame):
    def __init__(self, parent, config, task_manager, clicker_manager, windows_manager, game_objects, locale):
        super().__init__(parent, padding=(1,1), border=1, borderwidth=1, relief=SOLID)
        self.user_config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.clicker_manager: ClickerManager = clicker_manager
        self.windows_manager: WindowManager = windows_manager
        self.game_objects: GameObjectService = game_objects
        self.locale: Localization = locale
        self.windows_index = 0

        self.put_widgets()


    def water(self):
        # Инициализирую рабочее окно
        self.windows_manager.init_multi_windows()
        for window in self.windows_manager.windows_list:
            if not self.task_manager.stop_event.is_set():
                window: Window = window
                window.window.moveTo(newLeft=10,newTop=10)
                time.sleep(1)
                logger.info(msg="GATHER: WINDOW MOVED TO [10,10].")
            else:
                break
        while not self.task_manager.stop_event.is_set():
            self.task_manager.app.validator.get_time()
            if not self.windows_manager.windows_list:
                break
            else:
                window: Window = self.windows_manager.windows_list[0]
                time.sleep(2)
            try:
                window.window.activate()
                time.sleep(3)

            except PyGetWindowException as error:
                print("error open windows")

            self.game_objects.water_algorithm(window=window)
        messagebox.showinfo(title="Water war Task", message=self.locale.i10n('ww-end-window'))



    def start_task(self):
        self.task_manager.start_task(task_func=self.water, on_complete_func=self.end_task, name_service='Water War Service')

    def end_task(self):
        pass

    def put_widgets(self):
        image_path = resource_path("app\\img\\buttons\\water-on.png")
        self.image = tk.PhotoImage(file=image_path)  # Укажите путь к вашему изображению

         # Создаем кнопку с изображением
        button = tk.Button(self, image=self.image, command=self.start_task)
        button.grid(row=0, column=0)