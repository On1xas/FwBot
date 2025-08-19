import time
from tkinter import ttk
import tkinter as tk
from tkinter import Label, Entry, Button, SOLID, EW, messagebox, DISABLED, NORMAL
from app.utils.resourse_path import resource_path

from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager
from app.service.game_object_service import GameObjectService
from app.service.window_manager import WindowManager, Window
from app.service.locale_service import Localization
from app.utils.cv import find_template_matches, find_template_matches_color
from app.logging import logger


class ShelterRadarFrame(ttk.Frame):
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


    def radar_task(self):
        self.windows_manager.init_multi_windows()
        self.windows_index = 0
        for window in self.windows_manager.windows_list:
            if not self.task_manager.stop_event.is_set():
                window: Window = window
                window.window.moveTo(newLeft=10,newTop=10)
                time.sleep(1)
                logger.info(msg="RADAR: WINDOW MOVED TO [10,10].")
            else:
                break
        while not self.task_manager.stop_event.is_set():
            self.task_manager.app.validator.get_time()
            if not self.windows_manager.windows_list:
                break
            if self.windows_index > len(self.windows_manager.windows_list)-1:
                logger.info("RADAR: WINDOW INDEX END")
                break
            window: Window = self.windows_manager.windows_list[self.windows_index]
            time.sleep(3)
            window.window.activate()
            time.sleep(3)
            self.game_objects.radar_algorithm(window=window)

            self.windows_index += 1
            logger.info("RADAR: WINDOW INDEX UP: %s", self.windows_index)
         #Уведомление что все выполнено
        messagebox.showinfo(title="Radar Task", message="Радар выполнен")





    def start_task(self):
        self.task_manager.start_task(task_func=self.radar_task, on_complete_func=self.end_task, name_service='Radar Clicker')

    def end_task(self):
        pass


    def put_widgets(self):
        image_path = resource_path("app/img/buttons/radar-on.png")
        original_image = tk.PhotoImage(file=image_path)  # Укажите путь к вашему изображению
        self.image = original_image.subsample(original_image.width() // 50, original_image.height() // 50)
         # Создаем кнопку с изображением
        button = tk.Button(self, image=self.image, command=self.start_task)
        button.grid(row=0, column=0)