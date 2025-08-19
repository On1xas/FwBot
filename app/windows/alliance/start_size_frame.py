import time

from tkinter import ttk
from tkinter import Button, SOLID, messagebox

from app.config.config_manager import ConfigManager
from app.service.window_manager import Window, WindowManager
from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.service.locale_service import Localization
from app.service.game_object_service_OLD import GameObjectService
from app.utils.resourse_path import resource_path
from app.utils.cv import find_template_matches
from app.logging import logger

class StartSizeFrame(ttk.Frame):
    def __init__(self, parent, config, task_manager, clicker_manager, windows_manager, locale, game_object):
        self.frame: ttk.Frame = super().__init__(parent, padding=(2,2), border=2, borderwidth=1, relief=SOLID)
        self.user_config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.clicker_manager: ClickerManager = clicker_manager
        self.windows_manager: WindowManager = windows_manager
        self.game_objects: GameObjectService = game_object
        self.locale: Localization = locale
        self.put_widgets()

    def size_window(self):
        logger.info("ALLIANCE CLICKER: SHIFT WINDOWS START")
        for window in  self.windows_manager.windows_list:
            if not self.task_manager.stop_event.is_set():
                window: Window = window
                window.window.activate()
                time.sleep(2)
                self.game_objects.go_to_region()
                time.sleep(2)
                self.game_objects.go_to_ally()
                path_entry_ally_help = resource_path(relative_path="app\\img\\game_button\\ally\\alliance-hand.png")
                coord_entry_ally_help = find_template_matches(path_entry_ally_help, threshold=0.80)
                if coord_entry_ally_help and not self.task_manager.stop_event.is_set():
                    logger.info("ALLIANCE CLICKER: ENTRY HAND ALLY")
                    self.clicker_manager.click(coord_entry_ally_help[0][0], coord_entry_ally_help[0][1])
                    time.sleep(2)

                else:
                    logger.info("ALLIANCE CLICKER: HELP ALLY UNDEFIND")
                window.resize(
                    x=self.user_config.config.alliance_config.size_window_x,
                    y=self.user_config.config.alliance_config.size_window_y
                    )
            else:
                logger.info("ALLIANCE CLICKER: SIZE WINDOWS - INTERAPTED")
                break
        else:
            logger.info("ALLIANCE CLICKER: SIZE WINDOWS COMPLETED")
        self.windows_manager.move_all_windows()



    def maximized_window(self):
        logger.info("ALLIANCE CLICKER: MAXIMIZED WINDOWS START")
        for window in self.windows_manager.windows_list:
            if not self.task_manager.stop_event.is_set():
                window: Window = window
                window.resize(x=1280,y=720)
                time.sleep(1)
                window.window.moveTo(newLeft=10,newTop=10)
                time.sleep(1)
                logger.info(msg="ALLIANCE CLICKER: WINDOW MOVED TO [10,10].")

            else:
                messagebox.showerror(title="Maximize Task", message="Задача досрочно завершена")
                return
        messagebox.showinfo(title="", message="Расстановка окон завершена")



    def task_size_window(self):
        logger.info("ALLIANCE CLICKER: TASK [SIZE WINDOWS] START")
        self.task_manager.start_task(task_func=self.size_window, on_complete_func=self.end_task_size_window, name_service="Size Windows Service")

    def end_task_size_window(self):
        logger.info("ALLIANCE CLICKER: TASK [SIZE WINDOWS] END")

    def task_maximized_window(self):
        logger.info("ALLIANCE CLICKER: TASK [MAXIMIZED WINDOWS] START")
        self.task_manager.start_task(task_func=self.maximized_window, on_complete_func=self.end_task_size_window, name_service="Size Windows Service")

    def end_task_maximized_window(self):
        logger.info("ALLIANCE CLICKER: TASK [MAXIMIZED WINDOWS] END")

    def put_widgets(self):
        self.btn_start_win_with_loggin = Button(self, text=self.locale.i10n('shift-windows'), command=self.task_size_window)
        self.btn_start_win_with_loggin.grid(row=0,column=0)
        self.btn_start_win_with_loggin = Button(self, text=self.locale.i10n('sized-window'), command=self.task_maximized_window)
        self.btn_start_win_with_loggin.grid(row=1,column=0)