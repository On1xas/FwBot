import tkinter as tk
from tkinter import Tk, PhotoImage, ttk, EW, E,S, NSEW
from tkinter import messagebox

from app.config.config_manager import ConfigManager
from app.service.validator_manager import ValidatorManager
from app.config import locale
from app.logging import logger
from app.service.task_manager import TaskManager
from app.service.clicker_manager import ClickerManager
from app.service.window_manager import WindowManager
from app.service.game_object_service import GameObjectService
from app.service.locale_service import Localization

from app.windows.main_frames.user_frame import UserFrame
from app.windows.main_frames.footer_frame import FooterFrame

from app.windows.alliance.alliance_main_frame import AllianceMainFrame
from app.utils.resourse_path import resource_path
from app.windows.shelter.shelters_main_frame import SheltersMainFrame
from app.windows.license.license_frame import LicenseMainFrame


from app.utils.validate import is_validate

class MyApp(tk.Tk):
    def __init__(self: Tk, config):
        super().__init__()
        self.user_config: ConfigManager = config
        self.locale: Localization = locale
        self.task_manager: TaskManager = TaskManager(app=self, user_config=self.user_config, locale=self.locale)
        self.windows_manager: WindowManager = WindowManager(app=self, user_config=self.user_config, task_manager=self.task_manager)
        self.clicker_manager: ClickerManager = ClickerManager(user_config=self.user_config)
        self.validator: ValidatorManager = ValidatorManager(app=self, config=self.user_config, task_manager=self.task_manager)
        self.game_objects: GameObjectService= GameObjectService(windows_manager=self.windows_manager, task_manager=self.task_manager, clicker_manager=self.clicker_manager, parent=self, locale=self.locale)
        self.title("FW Clicker v0.0.1")
        self.geometry("400x350")
        self.resizable(width=False, height=False)
        self.icon_path = resource_path("app/icon.png")
        icon = PhotoImage(file = self.icon_path)
        self.iconphoto(False, icon)
        self.attributes("-fullscreen", False)
        self.show_frame = None
        self.frames = {
            "user_frame": None,
            "main_frame": None,
            "footer_frame": None
        }
        self.validate = False
        self.config(menu=self.create_menu())

        try:
            self.valid = self.validator.auth()
            if self.valid['status'] == "Authorize":
                logger.info(msg="APP: ******USER AUTORIZE*****")
                self.validate = True
                self.user_config.config.user.expired_time = self.valid['exp_time']
            elif self.valid['status'] == "Firstly":
                self.validate = False
                self.validator.server_status = True
            else:
                logger.info(msg="APP: ******USER FAIL AUTORIZE*****")
                messagebox.showerror(title=self.locale.i10n('desktop-msbse-auth-error-title'), message=f"{self.valid['error']}")
                self.validate = False
        except Exception as e:
            self.validate = False
            logger.info(msg=f"APP: FAIL CONNECTION TO SERVER {e}")
            messagebox.showinfo(title=self.locale.i10n('desktop-msbsi-serv-error-title'), message=self.locale.i10n('desktop-msbsi-serv-error-message'))
        self.render_main_widjet()
        self.render(frame=self.render_shelters_frame)

        # self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(100, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def render_main_widjet(self):
        logger.info(msg="APP: RENDER HEADER AND FOOTER WIDGET")
        self.user_frame = UserFrame(self)
        self.user_frame.grid(row=0, column=0, columnspan=2, sticky=EW)
        self.footer = FooterFrame(self)
        self.footer.grid(row=100,column=0, columnspan=2, sticky=EW+S)

    def change_locale(self, locale):
        logger.info("APP: UPDATE LOCALE TO %s", locale)
        self.user_config.update_locale(locale=locale)
        self.locale.switch_locale(new_locale=locale)
        self.footer.grid_forget()
        self.user_frame.grid_forget()
        self.config(menu="")
        self.config(menu=self.create_menu())
        self.render_main_widjet()
        self.render(frame=self.render_shelters_frame)


    def create_menu(self):
        self.main_menu = tk.Menu()
        self.main_menu.add_cascade(label=self.locale.i10n("shelter"), command=lambda: self.render(frame=self.render_shelters_frame))
        # self.main_menu.add_cascade(label=self.locale.i10n("alliance"), command=lambda: self.render(frame=self.render_alliance_frames))
        self.main_menu.add_cascade(label=self.locale.i10n("license"), command=lambda: self.render(frame=self.render_license_frame))

        language = tk.Menu(tearoff=0)
        language.add_cascade(label=f"Русский{' - ✓'.strip() if self.user_config.config.user.locale == 'ru' else ''}", command=lambda: self.change_locale(locale="ru"))
        language.add_cascade(label=f"English{' - ✓'.strip() if self.user_config.config.user.locale == 'en' else ''}", command=lambda: self.change_locale(locale="en"))

        settings = tk.Menu(tearoff=0)
        settings.add_cascade(label=self.locale.i10n("language"), menu=language)
        settings.add_cascade(label=self.locale.i10n("config"))
        # settings.add_cascade(label="Аккаунт")
        # settings.add_separator()
        # settings.add_cascade(label="Обновление")



        self.main_menu.add_cascade(label=self.locale.i10n("settings"), menu=settings)
        logger.info(msg="APP: RENDER MAIN MENU FRAME")
        return self.main_menu


    def render_alliance_frames(self):
        if self.show_frame is not None:
            self.hide_show_frame()
        logger.info(msg="APP: RENDER ALLIANCES FRAME")
        self.aliiance_frame = AllianceMainFrame(self)
        self.aliiance_frame.grid(row=1, rowspan=2, column=0, columnspan=2, sticky=NSEW, padx=1,pady=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.show_frame = self.aliiance_frame

    def render_shelters_frame(self):
        logger.info(msg="APP: RENDER SHELTERS FRAME")
        self.shelters_frame = SheltersMainFrame(self)
        self.shelters_frame.grid(row=1,rowspan=2, column=0, columnspan=2, sticky=NSEW)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.show_frame = self.shelters_frame

    def render_license_frame(self):
        logger.info(msg="APP: RENDER LICENSE FRAME")
        self.license_frame = LicenseMainFrame(self)
        self.license_frame.grid(row=1,rowspan=2, column=0, columnspan=2, sticky=NSEW)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.show_frame = self.license_frame

    def hide_show_frame(self):
        self.show_frame.grid_forget()

    def render(self, frame):
        if self.validate:
            if self.show_frame is not None:
                self.hide_show_frame()
            frame()
        else:
            self.render_license_frame()
