import time
from tkinter import ttk
import tkinter as tk
from tkinter import SOLID, EW, messagebox, StringVar, BooleanVar

from app.utils.resourse_path import resource_path
from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager
from app.service.game_object_service_OLD import GameObjectService
from app.service.locale_service import Localization
from app.service.window_manager import WindowManager, Window

from app.logging import logger


class ShelterRallyFrame(ttk.Frame):
    def __init__(self, parent, config, task_manager, clicker_manager, windows_manager, game_objects, locale):
        super().__init__(parent, padding=(1,1), border=1, borderwidth=1, relief=SOLID)
        self.user_config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.clicker_manager: ClickerManager = clicker_manager
        self.windows_manager: WindowManager = windows_manager
        self.game_objects: GameObjectService = game_objects
        self.locale: Localization = locale
        self.windows_index = 0
        self.languages = [
            self.locale.i10n('rally-lvlname-1'),
            self.locale.i10n('rally-lvlname-2'),
            self.locale.i10n('rally-lvlname-3'),
            self.locale.i10n('rally-lvlname-4'),
            self.locale.i10n('rally-lvlname-5'),
            self.locale.i10n('rally-lvlname-6'),
            self.locale.i10n('rally-lvlname-7'),
        ]
        self.put_widgets()

    def validate_input(self, char: str):
        return char.isdigit()


    def on_validate_input(self, P):
        # Проверяем, является ли ввод пустым или содержится в списке значений
        if P == "" or P in self.languages:
            return True
        else:
            return False

    def choose_param_window(self):

        self.choose_window: tk.Toplevel = tk.Toplevel()

        window_width = 300
        window_height = 200

        screen_width = self.choose_window.winfo_screenwidth()
        screen_height = self.choose_window.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.choose_window.title = self.locale.i10n('rally-window-title')
        self.choose_window.geometry(f"{215}x{250}+{x}+{y}")
        self.choose_window.resizable(width=False, height=False)
        self.choose_window.overrideredirect(boolean=True)
        validate_command = self.choose_window.register(self.validate_input)

        self.path_select_img = resource_path("app\\windows\\shelter\\healer\\img\\select.png")
        self.path_unselect_img = resource_path("app\\windows\\shelter\\healer\\img\\unselect.png")
        self.img_select = tk.PhotoImage(file=self.path_select_img)
        self.img_unselect = tk.PhotoImage(file=self.path_unselect_img, width=30, height=30)

        self.btn_start = ttk.Button(master=self.choose_window, text=self.locale.i10n('window-start'), command=self.get_data)
        self.btn_cancel = ttk.Button(master=self.choose_window, text=self.locale.i10n('window-cancel'), command=lambda: self.choose_window.destroy())
        self.var_entry_rally = BooleanVar()
        lbl_input_lvl = tk.Label(master=self.choose_window, text=self.locale.i10n('rally-window-lbl-lvl'), justify='center', anchor='center')
        lbl_input_count_rally = tk.Label(master=self.choose_window, text=self.locale.i10n('rally-window-lbl-input-count'), justify='center', anchor='center')
        lbl_entry_rally = tk.Label(master=self.choose_window, text=self.locale.i10n('rally-window-lbl-entry'), justify='center', anchor='center')
        self.combox_entry = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_entry_rally,
                                          borderwidth=0)

        self.languages_var = StringVar()
        self.combobox = ttk.Combobox(master=self.choose_window, values=self.languages[::-1], textvariable=self.languages_var)
        # Ограничиваем ввод любых данных в строку выпадающего списка
        vcmd = (self.choose_window.register(self.on_validate_input), '%P')
        self.combobox['validate'] = 'key'
        self.combobox['validatecommand'] = vcmd



        self.inpt_btn = tk.Entry(master=self.choose_window, justify='center', validate='key', validatecommand=(validate_command, '%S'))

        lbl_input_lvl.grid(columnspan=4, row=0, sticky=EW, padx=35, pady=2)
        self.combobox.grid(columnspan=4, row=1, sticky=EW, padx=35, pady=2)
        lbl_input_count_rally.grid(columnspan=4, row=2, sticky=EW, padx=25, pady=2)
        self.inpt_btn.grid(columnspan=4, row=3, sticky=EW, padx=35, pady=2)
        lbl_entry_rally.grid(columnspan=4, row=4, sticky=EW, padx=35, pady=2)
        self.combox_entry.grid(columnspan=4, row=5, sticky=EW, padx=35, pady=2)
        self.btn_start.grid(row=7,column=0, columnspan=2, sticky=EW, padx=5)
        self.btn_cancel.grid(row=7,column=2, columnspan=2, sticky=EW, padx=5)

    def get_data(self):

        lvl = {
            self.locale.i10n('rally-lvlname-1'): 1,
            self.locale.i10n('rally-lvlname-2'): 2,
            self.locale.i10n('rally-lvlname-3'): 3,
            self.locale.i10n('rally-lvlname-4'): 4,
            self.locale.i10n('rally-lvlname-5'): 5,
            self.locale.i10n('rally-lvlname-6'): 6,
            self.locale.i10n('rally-lvlname-7'): 7,
        }

        data = {
            "max_lvl" : self.languages_var.get(),
            "count_rally": int(self.inpt_btn.get()),
            "fail_count": 0,
            "down_triger": False,
            "down_count": 0,
            "start_time_rally": "",
            "entry_rally": self.var_entry_rally.get()
            }
        if data['max_lvl'] == "":
            messagebox.showerror(title=self.locale.i10n('rally-msgbse-error-data-title'), message=self.locale.i10n('rally-msgbse-error-maxlvlerror-message'))
            return
        else:
            data['max_lvl'] = lvl[self.languages_var.get()]
        if self.inpt_btn.get() == "":
            data['count_rally'] = 0
        if int(data['count_rally']) <= 0:
            messagebox.showerror(title=self.locale.i10n('rally-msgbse-error-data-title'), message=self.locale.i10n('rally-msgbse-error-counterror-message'))
            return

        self.rally_data = data

        self.choose_window.destroy()
        # МЕСТО ЗАПУСКА THREAD
        self.start_task()


    def rally_task(self):
        self.windows_manager.init_multi_windows()
        self.windows_index = 0
        for window in self.windows_manager.windows_list:
            if not self.task_manager.stop_event.is_set():
                window: Window = window
                window.window.moveTo(newLeft=10,newTop=10)
                time.sleep(1)
                logger.info(msg="RALLY: WINDOW MOVED TO [10,10].")
            else:
                logger.info(msg="RALLY: TAST MANUALLY INTERAPTED")
                return
        self.task_manager.app.validator.get_time()
        if not self.windows_manager.windows_list:
            logger.error(msg="RALLY: WINDOW NOT DETECTED")
            return
        window: Window = self.windows_manager.windows_list[0]
        time.sleep(3)
        window.window.activate()
        time.sleep(3)
        logger.info("RALLY: GET TASK - %s", self.rally_data)
        self.game_objects.rally_step_0(window=window, task=self.rally_data)

        #Уведомление что все выполнено
        self.game_objects.rally_task = {}
        messagebox.showinfo(title=self.locale.i10n('rally-task-end-title'), message=self.locale.i10n('rally-task-end-message'))





    def start_task(self):
        self.task_manager.start_task(task_func=self.rally_task, on_complete_func=self.end_task, name_service='Rally Clicker')

    def end_task(self):
        pass


    def put_widgets(self):
        image_path = resource_path("app/img/buttons/razym-on.png")
        original_image = tk.PhotoImage(file=image_path)  # Укажите путь к вашему изображению
        self.image = original_image.subsample(original_image.width() // 50, original_image.height() // 50)
         # Создаем кнопку с изображением
        button = tk.Button(self, image=self.image, command=self.choose_param_window)
        button.grid(row=0, column=0)