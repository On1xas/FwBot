
import time
from tkinter import ttk
import tkinter as tk
from tkinter import SOLID, EW, messagebox

from pygetwindow import PyGetWindowException
from app.utils.resourse_path import resource_path
from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager
from app.service.game_object_service_OLD import GameObjectService
from app.service.locale_service import Localization
from app.service.window_manager import WindowManager, Window
from app.logging import logger

def check_stop_func(method):
    def wrapper(self, *args, **kwargs):
        if not self.task_manager.stop_func:
            logger.info(msg=f"GATHER: DECORATOR INIT {method.__name__}")
            return method(self, *args, **kwargs)
        else:
            logger.info(msg=f"GATHER: DECORATOR - STOP PROCESS START - STATUS STOP FUNC TRIGGER [{self.task_manager.stop_func}]")
            return None
    return wrapper

class ShelterDailyFrame(ttk.Frame):
    def __init__(self, parent, config, task_manager, clicker_manager, windows_manager, game_objects, locale):
        super().__init__(parent, padding=(1,1), border=1, borderwidth=1, relief=SOLID)
        self.user_config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.clicker_manager: ClickerManager = clicker_manager
        self.windows_manager: WindowManager = windows_manager
        self.game_objects: GameObjectService = game_objects
        self.locale: Localization = locale
        self.windows_index = 0
        self.daily_data = {}
        self.put_widgets()


    def choose_param_window(self):
        self.choose_window = tk.Toplevel()

        window_width = 200
        window_height = 200

        screen_width = self.choose_window.winfo_screenwidth()
        screen_height = self.choose_window.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.choose_window.title(self.locale.i10n('daily-window-title'))  # Исправлено: title() вместо присваивания
        self.choose_window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Исправлено: используем переменные
        self.choose_window.resizable(width=False, height=False)
        self.choose_window.overrideredirect(boolean=True)

        # Создаем основной фрейм для центрирования содержимого
        main_frame = tk.Frame(self.choose_window)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Настройка grid для равномерного распределения
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_columnconfigure(3, weight=1)

        for i in range(6):  # У нас 6 строк (0-5)
            main_frame.grid_rowconfigure(i, weight=1)

        self.path_select_img = resource_path("app\\windows\\shelter\\healer\\img\\select.png")
        self.path_unselect_img = resource_path("app\\windows\\shelter\\healer\\img\\unselect.png")
        self.img_select = tk.PhotoImage(file=self.path_select_img)
        self.img_unselect = tk.PhotoImage(file=self.path_unselect_img, width=30, height=30)

        self.btn_start = ttk.Button(master=main_frame, text=self.locale.i10n('window-start'), command=self.get_data)
        self.btn_cancel = ttk.Button(master=main_frame, text=self.locale.i10n('window-cancel'), command=lambda: self.choose_window.destroy())

        lbl_radar = tk.Label(master=main_frame, text=self.locale.i10n('daily-window-lbl-radar'), justify='center')
        lbl_arena = tk.Label(master=main_frame, text=self.locale.i10n('daily-window-lbl-arena'), justify='center')

        self.var_radar = tk.BooleanVar()
        self.var_arena = tk.BooleanVar()

        self.combox_radar = tk.Checkbutton(master=main_frame,
                                        image=self.img_unselect,
                                        selectimage=self.img_select,
                                        indicatoron=False,
                                        bg=self.choose_window.cget('bg'),
                                        selectcolor=self.choose_window.cget('bg'),
                                        variable=self.var_radar,
                                        borderwidth=0)
        self.combox_arena = tk.Checkbutton(master=main_frame,
                                        image=self.img_unselect,
                                        selectimage=self.img_select,
                                        indicatoron=False,
                                        bg=self.choose_window.cget('bg'),
                                        selectcolor=self.choose_window.cget('bg'),
                                        variable=self.var_arena,
                                        borderwidth=0)

        # Размещаем элементы с центрированием
        lbl_radar.grid(column=0, row=0, columnspan=4, sticky='nsew', padx=5, pady=2)
        self.combox_radar.grid(column=0, row=1, columnspan=4, sticky='n', padx=3, pady=2)
        lbl_arena.grid(column=0, row=2, columnspan=4, sticky='nsew', padx=5, pady=2)
        self.combox_arena.grid(column=0, row=3, columnspan=4, sticky='n', padx=3, pady=2)

        # Кнопки размещаем в нижней части
        self.btn_start.grid(column=0, row=5, columnspan=2, sticky='ew', padx=5, pady=5)
        self.btn_cancel.grid(column=2, row=5, columnspan=2, sticky='ew', padx=5, pady=5)


    # def choose_param_window(self):

    #     self.choose_window: tk.Toplevel = tk.Toplevel()

    #     window_width = 300
    #     window_height = 200

    #     screen_width = self.choose_window.winfo_screenwidth()
    #     screen_height = self.choose_window.winfo_screenheight()

    #     x = (screen_width // 2) - (window_width // 2)
    #     y = (screen_height // 2) - (window_height // 2)

    #     self.choose_window.title = self.locale.i10n('daily-window-title')
    #     self.choose_window.geometry(f"{200}x{200}+{x}+{y}")
    #     self.choose_window.resizable(width=False, height=False)
    #     self.choose_window.overrideredirect(boolean=True)

    #     self.path_select_img = resource_path("app\\windows\\shelter\\healer\\img\\select.png")
    #     self.path_unselect_img = resource_path("app\\windows\\shelter\\healer\\img\\unselect.png")
    #     self.img_select = tk.PhotoImage(file=self.path_select_img)
    #     self.img_unselect = tk.PhotoImage(file=self.path_unselect_img, width=30, height=30)

    #     self.btn_start = ttk.Button(master=self.choose_window, text=self.locale.i10n('window-start'), command=self.get_data)
    #     self.btn_cancel = ttk.Button(master=self.choose_window, text=self.locale.i10n('window-cancel'), command=lambda: self.choose_window.destroy())

    #     lbl_radar = tk.Label(master=self.choose_window, text=self.locale.i10n('daily-window-lbl-radar'), justify='center', anchor='center')
    #     lbl_arena = tk.Label(master=self.choose_window, text=self.locale.i10n('daily-window-lbl-arena'), justify='center', anchor='center')

    #     self.var_radar = tk.BooleanVar()
    #     self.var_arena = tk.BooleanVar()

    #     self.combox_radar = tk.Checkbutton(master=self.choose_window,
    #                                       image=self.img_unselect,
    #                                       selectimage=self.img_select,
    #                                       indicatoron=False,
    #                                       bg=self.choose_window.cget('bg'),
    #                                       selectcolor=self.choose_window.cget('bg'),
    #                                       variable=self.var_radar,
    #                                       borderwidth=0)
    #     self.combox_arena = tk.Checkbutton(master=self.choose_window,
    #                                       image=self.img_unselect,
    #                                       selectimage=self.img_select,
    #                                       indicatoron=False,
    #                                       bg=self.choose_window.cget('bg'),
    #                                       selectcolor=self.choose_window.cget('bg'),
    #                                       variable=self.var_arena,
    #                                       borderwidth=0)

    #     lbl_radar.grid(columnspan=4, row=0, sticky=EW, padx=5, pady=2)
    #     self.combox_radar.grid(columnspan=4, row=1, sticky=EW, padx=3, pady=2)
    #     lbl_arena.grid(columnspan=4, row=2, sticky=EW, padx=5, pady=2)
    #     self.combox_arena.grid(columnspan=4, row=3, sticky=EW, padx=3, pady=2)

    #     self.btn_start.grid(row=5,column=0, columnspan=2, sticky=EW)
    #     self.btn_cancel.grid(row=5,column=2, columnspan=2, sticky=EW)

    def get_data(self):


        data = {
            "task_radar" : self.var_radar.get(),
            "task_arena": self.var_arena.get()
            }

        self.daily_data = data
        self.choose_window.destroy()

        self.start_task()

    def daily_task(self, task):
        # Инициализирую рабочее окно
        self.windows_manager.init_multi_windows()
        self.windows_index = 0
        for window in self.windows_manager.windows_list:
            if not self.task_manager.stop_event.is_set():
                window: Window = window
                window.window.moveTo(newLeft=10,newTop=10)
                time.sleep(1)
                logger.info(msg="GATHER: WINDOW MOVED TO [10,10].")
            else:
                break
        # Основной цикл задания
        while not self.task_manager.stop_event.is_set():
            self.task_manager.app.validator.get_time()
            if not self.windows_manager.windows_list:
                break
            if self.windows_index > len(self.windows_manager.windows_list)-1:
                logger.info(msg="GATHER: ALL WINDOWS GATHERED. DROP INDEX WINDOW.")
                break
            window: Window = self.windows_manager.windows_list[self.windows_index]
            time.sleep(2)
            try:
                window.window.activate()
                time.sleep(3)

            except PyGetWindowException as error:
                print("error open windows")

            if self.daily_data['task_radar']:
                self.game_objects.radar_algorithm(window=window)

            self.game_objects.go_to_shelter()
            time.sleep(1)

            self.game_objects.click_hand()
            time.sleep(1)
            self.game_objects.hide_discont()
            time.sleep(1)
            self.game_objects.take_shop()
            time.sleep(1)
            self.game_objects.police_poisk()
            time.sleep(1)
            self.game_objects.buff_resourse()
            time.sleep(1)
            self.game_objects.take_expedition(window=window)
            time.sleep(1)
            self.game_objects.take_racia()
            time.sleep(1)
            self.game_objects.take_compamy(window=window, task_arena=self.daily_data['task_arena'])
            time.sleep(1)
            self.game_objects.take_alliance_bonus(window=window)
            time.sleep(1)
            self.game_objects.click_hand()
            time.sleep(1)
            self.game_objects.take_police_dron(window=window)
            time.sleep(1)
            self.game_objects.take_cex(window=window)
            time.sleep(1)
            self.game_objects.take_ferm()
            time.sleep(1)
            self.game_objects.take_mail(window=window)
            time.sleep(1)
            self.game_objects.take_vip(window=window)
            time.sleep(1)
            self.game_objects.take_daily_bonus(window=window)
            time.sleep(1)
            self.game_objects.take_special_action(window=window)
            time.sleep(1)

            self.game_objects.click_hand()

            self.windows_index += 1
        messagebox.showinfo(title=self.locale.i10n('daily-task-end-title'), message=self.locale.i10n('daily-task-end-message'))


    def start_task(self):
        self.task_manager.start_task(task_func=lambda: self.daily_task(task=self.daily_data), on_complete_func=self.end_task, name_service='Daily Clicker')

    def end_task(self):
        pass

    def put_widgets(self):
        image_path = resource_path("app/img/buttons/daily-on.png")
        self.image = tk.PhotoImage(file=image_path)  # Укажите путь к вашему изображению

         # Создаем кнопку с изображением
        button = tk.Button(self, image=self.image, command=self.choose_param_window)
        button.grid(row=0, column=0)