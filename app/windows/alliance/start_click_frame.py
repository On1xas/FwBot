import time
import pyautogui
from tkinter import ttk
from tkinter import Button, SOLID, DISABLED, NORMAL, messagebox
from pygetwindow import Win32Window
from app.config.config_manager import ConfigManager
from app.service.clicker_manager import ClickerManager
from app.service.window_manager import Window, WindowManager
from app.logging import logger
from app.service.task_manager import TaskManager
from app.service.locale_service import Localization
from app.service.game_object_service_OLD import GameObjectService
from app.utils.resourse_path import resource_path
from app.utils.cv import find_template_matches, filter_coordinates


class StartClickFrame(ttk.Frame):
    def __init__(self, parent, config, task_manager, clicker_manager, windows_manager, game_object, locale):
        super().__init__(parent, padding=(2,2), border=2, borderwidth=1, relief=SOLID)
        self.user_config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.clicker_manager: ClickerManager = clicker_manager
        self.windows_manager: WindowManager = windows_manager
        self.locale: Localization = locale
        self.game_objects: GameObjectService = game_object
        self.put_widgets()



    def clicker_cycle(self):
        logger.info(f"ALLIANCE CLICKER:: CLIKER THREAD START")
        path_click = resource_path(relative_path=self.locale.i10n('alliance-help'))

        while not self.task_manager.stop_event.is_set():
            time.sleep(1.5)
            coord_click = find_template_matches(path_click)
            coord_click_filtered = filter_coordinates(coords=coord_click, threshold=10)
            for x,y in coord_click_filtered:
                pyautogui.doubleClick(
                    x=x,
                    y=y
                )
                time.sleep(0.05)





            # for window in self.windows_manager.windows_list:
            #     window_obj: Window = window
            #     window: Win32Window = window_obj.window
            #     window.activate()
            #     # time.sleep(0.15)
            #     if not self.task_manager.stop_event.is_set():
            #         self.clicker_manager.proportion_alliance_doubleclick_in_window(window=window_obj.window,
            #                                                         target_x=620,
            #                                                         target_y=625)
            #         time.sleep(0.1)
            #     else:
            #         logger.info("ALLIANCE CLICKER: CYCLE INTERAPTED")
            #         break
            # logger.info("ALLIANCE CLICKER: SLEEP 5 SEC")
            # time.sleep(0.1)


    def task_start_clicker(self):
        self.btn_start_win_with_loggin.config(
            state=DISABLED,
            background='yellow',
            foreground='black',
            relief='sunken',
            text=self.locale.i10n('clicker_started')
            )

        logger.info(f"APP: ALLIANCE FRAME: TASK [HAND CLIKER] START")
        self.task_manager.start_task(task_func=self.clicker_cycle, on_complete_func=self.end_task_clicker, name_service='Ferms Hand Clicker')


    def end_task_clicker(self):
        self.btn_start_win_with_loggin.config(
            state=NORMAL,
            background='green',
            foreground='white',
            relief='raised',
            text=self.locale.i10n('start_clicker')
            )
        messagebox.showinfo(title=self.locale.i10n('messagebox_title_clicker_end'), message=self.locale.i10n('messagebox_clicker_end'))
        logger.info(f"APP: ALLIANCE FRAME: TASK [HAND CLIKER] END")

    def put_widgets(self):
        self.btn_start_win_with_loggin = Button(self, text=self.locale.i10n('start_clicker'), justify="center", anchor="center", background="green", foreground="white", command=self.task_start_clicker)
        self.btn_start_win_with_loggin.grid(row=0,column=0, ipadx=5, ipady=5)