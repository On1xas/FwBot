from tkinter import ttk
import tkinter as tk
from tkinter import SOLID

from app.utils.resourse_path import resource_path
from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager
from app.service.game_object_service_OLD import GameObjectService
from app.service.locale_service import Localization
from app.service.window_manager import WindowManager
from app.logging import logger


class ShelterGatherFrame(ttk.Frame):
    def __init__(self, parent, config, task_manager, clicker_manager, windows_manager, game_objects, locale):
        super().__init__(parent, padding=(1,1), border=1, borderwidth=1, relief=SOLID)
        self.user_config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.clicker_manager: ClickerManager = clicker_manager
        self.windows_manager: WindowManager = windows_manager
        self.game_objects: GameObjectService = game_objects
        self.locale: Localization = locale
        self.put_widgets()


    def put_widgets(self):
        image_path = resource_path("app/img/buttons/gather_on.png")
        self.image = tk.PhotoImage(file=image_path)  # Укажите путь к вашему изображению
        logger.info("APP: GATHER BUTTON PRESS")
         # Создаем кнопку с изображением
        button = tk.Button(self, image=self.image, command=lambda: self.game_objects.choose_param_gather(task="gather"))
        button.grid(row=0, column=0)