import time
import subprocess
import pygetwindow as gw
from tkinter import ttk
from tkinter import Label, Entry, Button, SOLID, EW
from tkinter import messagebox
from app.config.config_manager import ConfigManager
from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.service.window_manager import Window, WindowManager
from app.service.locale_service import Localization
from app.logging import logger

class StartWWithoutLogginFrame(ttk.Frame):
    def __init__(self, parent, config, task_manager: TaskManager, clicker_manager: ClickerManager, windows_manager: WindowManager, locale):
        self.frame: ttk.Frame = super().__init__(parent, padding=(2, 2), border=2, borderwidth=3, relief=SOLID)
        self.user_config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.clicker_manager: ClickerManager = clicker_manager
        self.windows_manager: WindowManager = windows_manager
        self.locale: Localization = locale
        self.put_widgets()


    def open_window_without_login(self):
        window_title = "Doomsday: Last Survivors"
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            for window in windows:
                logger.info(f"APP: ALLIANCE FRAME: START_WINDOW_WITHOUT_LOGGIN - UNREGISTERED WINDOW CLOSE")
                window.close()
        try:
            logger.info(f"APP: ALLIANCE FRAME: START_WINDOW_WITHOUT_LOGGIN START")
            for i in range(self.user_config.config.alliance_config.count_open_window):
                if not self.task_manager.stop_event.is_set():
                    subprocess.Popen(self.user_config.config.alliance_config.path_to_exe)
                    time.sleep(12+i)
                else:
                    logger.info(f"APP: ALLIANCE FRAME: START_WINDOW_WITHOUT_LOGGIN INTERAPTED")
                    break
            self.windows_manager.init_multi_windows()
            time.sleep(3)
            messagebox.showinfo(message=self.locale.i10n('messagebox-info', count=len(self.windows_manager.windows_list)))
        except OSError as e:
            logger.exception(msg=e)
            logger.error(f"APP: ALLIANCE FRAME: START_WINDOW_WITHOUT_LOGGIN - [ERROR] PERMISSION DENIED")
            messagebox.showinfo(title="Недостаточно прав доступа", message="Недостаточно прав для запуска окна.\nЗапустите программу с правами администратора")

    def start_add_open_window(self):
        self.windows_manager.init_alliance_clicker_multi_windows()
        time.sleep(2)
        messagebox.showinfo(message=self.locale.i10n('messagebox-info', count=len(self.windows_manager.windows_list)))

    def task_open_window_without_loggin(self):
        logger.info(f"APP: ALLIANCE FRAME: TASK [START_WINDOW_INIT] STARTED")
        self.task_manager.start_task(task_func=self.open_window_without_login, on_complete_func=self.end_task_open_window_without_loggin, name_service="Open Windows Service")

    def end_task_open_window_without_loggin(self):
        logger.info(f"APP: ALLIANCE FRAME: TASK [START_WINDOW_INIT] END")


    def put_widgets(self):

        label_X = Label(self, text=self.locale.i10n('init-windows'))
        label_X.grid(row=0, column=0, sticky="we")

        self.btn_start_win_without_loggin = Button(self, text=self.locale.i10n('start-windows'), command=self.task_open_window_without_loggin)
        self.btn_start_win_without_loggin.grid(row=1,column=0, pady=2)

        self.btn_start_win_with_loggin = Button(self, text=self.locale.i10n('connection-windows'), command=self.start_add_open_window)
        self.btn_start_win_with_loggin.config(state='normal')
        self.btn_start_win_with_loggin.grid(row=2,column=0, padx=2, pady=2)