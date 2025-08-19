from tkinter import ttk
from tkinter import Label, Entry, Button, SOLID, EW

from app.config.config_manager import ConfigManager
from app.windows.alliance.choose_open_window_frame import ChooseOpenWindows
from app.windows.alliance.size_window_frame import ChooseSizeWindow
from app.windows.alliance.entry_game_path import ChooseEXEPathFrame
from app.windows.alliance.start_w_frame import StartWWithoutLogginFrame
from app.windows.alliance.start_size_frame import StartSizeFrame
from app.windows.alliance.start_click_frame import StartClickFrame

from app.service.clicker_manager import ClickerManager
from app.service.window_manager import WindowManager
from app.service.locale_service import Localization
from app.service.game_object_service_OLD import GameObjectService

class AllianceMainFrame(ttk.Frame):
    def __init__(self, parent):
        self.frame: ttk.Frame = super().__init__(parent, padding=(3,3), border=2, borderwidth=3, relief=SOLID)
        self.app = parent
        self.task_manager = self.app.task_manager
        self.user_config: ConfigManager = self.app.user_config
        self.clicker_manager: ClickerManager = self.app.clicker_manager
        self.windows_manager:WindowManager = self.app.windows_manager
        self.locale: Localization = self.app.locale
        self.game_objects: GameObjectService = self.app.game_objects
        self.put_alliance_frame()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


    def put_alliance_frame(self):
        self.choose_count_open_windows:ttk.Frame = ChooseOpenWindows(self, self.user_config, locale=self.locale)
        self.choose_size_window = ChooseSizeWindow(self, self.user_config, locale=self.locale)
        self.entry_exe_path_window = ChooseEXEPathFrame(self, self.user_config, locale=self.locale)

        self.start_w_wout_loggin = StartWWithoutLogginFrame(
            parent=self,
            config=self.user_config,
            task_manager=self.task_manager,
            clicker_manager=self.clicker_manager,
            windows_manager=self.windows_manager,
            locale=self.locale
            )
        self.start_sizes = StartSizeFrame(
            parent=self,
            config=self.user_config,
            task_manager=self.task_manager,
            clicker_manager=self.clicker_manager,
            windows_manager=self.windows_manager,
            locale=self.locale,
            game_object=self.game_objects
            )
        self.start_click = StartClickFrame(
            parent=self,
            config=self.user_config,
            task_manager=self.task_manager,
            clicker_manager=self.clicker_manager,
            windows_manager=self.windows_manager,
            game_object=self.game_objects,
            locale=self.locale
            )

        self.choose_count_open_windows.grid(row=1,column=0, sticky=EW, padx=3,pady=3)
        self.choose_size_window.grid(row=2, column=0,sticky=EW, padx=3,pady=3)
        self.entry_exe_path_window.grid(row=3, column=0,sticky=EW, padx=3,pady=3)
        self.start_w_wout_loggin.grid(row=1,column=1, padx=3, pady=3)
        self.start_sizes.grid(row=2,column=1, padx=3, pady=3)
        self.start_click.grid(row=3,column=1, padx=3, pady=3)