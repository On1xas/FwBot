
import time
from tkinter import ttk
import tkinter as tk
from tkinter import Label, Entry, Button, SOLID, EW, messagebox, DISABLED, NORMAL
from app.utils.resourse_path import resource_path

from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager
from app.service.window_manager import WindowManager, Window

class InitWindowFrame(ttk.Frame):
    def __init__(self, parent, config, task_manager, clicker_manager, windows_manager):
        super().__init__(parent, padding=(1,1), border=1, borderwidth=1, relief=SOLID)
        self.user_config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.clicker_manager: ClickerManager = clicker_manager
        self.windows_manager: WindowManager = windows_manager
        self.heal_data = dict()
        self.put_widgets()

    def put_widgets(self):
        button = tk.Button(self, text="Запустить игру")
        button.grid(row=0, column=1)