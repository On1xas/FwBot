
import time
from tkinter import ttk
import tkinter as tk
from tkinter import Label, Entry, SOLID, EW, messagebox

from app.utils.resourse_path import resource_path
from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager
from app.service.game_object_service_OLD import GameObjectService
from app.service.locale_service import Localization
from app.service.window_manager import WindowManager, Window

from app.logging import logger

class ShelterTransferFrame(ttk.Frame):
    def __init__(self, parent, config, task_manager, clicker_manager, windows_manager, game_objects, locale):
        super().__init__(parent, padding=(1,1), border=1, borderwidth=1, relief=SOLID)
        self.user_config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.clicker_manager: ClickerManager = clicker_manager
        self.windows_manager: WindowManager = windows_manager
        self.game_objects: GameObjectService = game_objects
        self.locale: Localization = locale
        self.put_widgets()
        self.var_food = tk.BooleanVar()
        self.var_wood = tk.BooleanVar()
        self.var_steel = tk.BooleanVar()
        self.var_oil = tk.BooleanVar()
        self.transfer_data = {}

    def choose_resourse(self, resourse):
        if resourse == "food" and self.var_food.get() == True:
            self.var_wood.set(value=False)
            self.var_steel.set(value=False)
            self.var_oil.set(value=False)
        elif resourse == "wood" and self.var_wood.get() == True:
            self.var_food.set(value=False)
            self.var_steel.set(value=False)
            self.var_oil.set(value=False)
        elif resourse == "steel" and self.var_steel.get() == True:
            self.var_food.set(value=False)
            self.var_wood.set(value=False)
            self.var_oil.set(value=False)
        elif resourse == "oil" and self.var_oil.get() == True:
            self.var_food.set(value=False)
            self.var_wood.set(value=False)
            self.var_steel.set(value=False)

    def validate_input(self, char: str):
        return char.isdigit()


    def choose_param_gather(self):
        self.choose_window: tk.Toplevel = tk.Toplevel()

        window_width = 300
        window_height = 350

        screen_width = self.choose_window.winfo_screenwidth()
        screen_height = self.choose_window.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.choose_window.title = self.locale.i10n('transfer-window-title')
        self.choose_window.geometry(f"{195}x{220}+{x}+{y}")
        self.choose_window.resizable(width=False, height=False)
        self.choose_window.overrideredirect(boolean=True)
        validate_command = self.choose_window.register(self.validate_input)

        self.btn_start = ttk.Button(master=self.choose_window, text=self.locale.i10n('window-start'), command=self.get_data)
        self.btn_cancel = ttk.Button(master=self.choose_window, text=self.locale.i10n('window-cancel'), command=lambda: self.choose_window.destroy())
        lbl_terry_alliance = tk.Label(master=self.choose_window, text=self.locale.i10n('transfer-window-lbl-terry-alliance'), justify='center', anchor='center', pady=10)




        self.path_food_img = resource_path("app\\windows\\shelter\\gather\\img\\food.png")
        self.img_food = tk.PhotoImage(file=self.path_food_img)
        self.path_wood_img = resource_path("app\\windows\\shelter\\gather\\img\\wood.png")
        self.img_wood = tk.PhotoImage(file=self.path_wood_img)
        self.path_steel_img = resource_path("app\\windows\\shelter\\gather\\img\\steel.png")
        self.img_steel = tk.PhotoImage(file=self.path_steel_img)
        self.path_oil_img = resource_path("app\\windows\\shelter\\gather\\img\\oil.png")
        self.img_oil = tk.PhotoImage(file=self.path_oil_img)


        lbl_food = tk.Label(master=self.choose_window, image=self.img_food)
        lbl_wood = tk.Label(master=self.choose_window, image=self.img_wood)
        lbl_steel = tk.Label(master=self.choose_window, image=self.img_steel)
        lbl_oil = tk.Label(master=self.choose_window, image=self.img_oil)

        self.path_select_img = resource_path("app\\windows\\shelter\\healer\\img\\select.png")
        self.path_unselect_img = resource_path("app\\windows\\shelter\\healer\\img\\unselect.png")




        self.img_select = tk.PhotoImage(file=self.path_select_img)
        self.img_unselect = tk.PhotoImage(file=self.path_unselect_img, width=30, height=30)

        self.chckbtn_food = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_food,
                                          borderwidth=0,
                                          command=lambda: self.choose_resourse(resourse="food"))
        self.chckbtn_wood = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_wood,
                                          borderwidth=0,
                                          command=lambda: self.choose_resourse(resourse="wood"))
        self.chckbtn_steel = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_steel,
                                          borderwidth=0,
                                          command=lambda: self.choose_resourse(resourse="steel"))
        self.chckbtn_oil = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_oil,
                                          borderwidth=0,
                                          command=lambda: self.choose_resourse(resourse="oil"))


        self.label_x = Label(master=self.choose_window, text="X:", justify='center')
        self.entry_x = Entry(master=self.choose_window, justify='center', width=11, validate='key', validatecommand=(validate_command, '%S'))
        self.label_y = Label(master=self.choose_window, text="Y:", justify='center')
        self.entry_y = Entry(master=self.choose_window, justify='center', width=11, validate='key', validatecommand=(validate_command, '%S'))

        lbl_food.grid(row=1,column=0, padx=5, pady=1, sticky=EW)
        lbl_wood.grid(row=1,column=1, padx=5, pady=1, sticky=EW)
        lbl_steel.grid(row=1,column=2, padx=5, pady=1, sticky=EW)
        lbl_oil.grid(row=1,column=3, padx=5, pady=1, sticky=EW)

        self.chckbtn_food.grid(row=2,column=0, padx=5, pady=1, sticky=EW)
        self.chckbtn_wood.grid(row=2,column=1, padx=5, pady=1, sticky=EW)
        self.chckbtn_steel.grid(row=2,column=2, padx=5, pady=1, sticky=EW)
        self.chckbtn_oil.grid(row=2,column=3, padx=5, pady=1, sticky=EW)

        lbl_terry_alliance.grid(row=3, columnspan=5, sticky=EW)

        self.label_x.grid(row=4, column=0, columnspan=2, sticky=EW)
        self.entry_x.grid(row=5, column=0, columnspan=2, pady=5)
        self.label_y.grid(row=4, column=2, columnspan=2, sticky=EW)
        self.entry_y.grid(row=5, column=2, columnspan=2, pady=5)

        self.btn_start.grid(row=6,column=0, columnspan=2, padx=5, pady=5)
        self.btn_cancel.grid(row=6,column=2, columnspan=2, padx=5, pady=5)




    def get_data(self):
        data = {
            "food": self.var_food.get(),
            "wood": self.var_wood.get(),
            "steel": self.var_steel.get(),
            "oil": self.var_oil.get(),
            }
        self.transfer_task = {
            "task": "",
            "coord": (self.entry_x.get(), self.entry_y.get())
        }

        for k,v in data.items():
            if v:
                self.transfer_task['task'] = k
                break

        self.choose_window.destroy()

        if self.transfer_task['task']:
        # МЕСТО ЗАПУСКА THREAD
            self.start_task()

            logger.info(msg=f"TRANSFER: GET DATA IS GOOD")
        else:
            messagebox.showwarning(title=self.locale.i10n('transfer-msgbsw-task-error-title'), message=self.locale.i10n('transfer-msgbsw-task-error-message'))
            self.choose_window.destroy()

    def transfer_algorithm(self):
        self.transfer_list = []
        self.task_status = False
        self.count_end = 0
        self.windows_manager.init_multi_windows()
        self.windows_index = 0
        for id, window in enumerate(self.windows_manager.windows_list, start=1):
            if not self.task_manager.stop_event.is_set():
                window: Window = window
                task = {
                    "id": id,
                    "window": window,
                    "screen_status": None,
                    "transfer_status": False,
                    "resourse_status": False,
                    "hide_discount": False,
                    "task_status": self.task_status,
                     "fail_count": 0,
                    }
                task.update(self.transfer_task)
                self.transfer_list.append(task)
                window.window.moveTo(newLeft=10,newTop=10)
                time.sleep(1)
                logger.info(msg="TRANSFER: WINDOW MOVED TO [10,10].")
            else:
                break
        while not self.task_manager.stop_event.is_set():
            self.task_manager.app.validator.get_time()
            if not self.windows_manager.windows_list:
                break

            if self.count_end > 20:
                logger.info("TRANSFER: END COUNT: %s. TASK INTERRAPT", self.count_end)
                break

            if self.windows_index > len(self.transfer_list)-1:
                logger.info("TRANSFER: WINDOW INDEX DROP")
                self.windows_index = 0

            window: Window = self.transfer_list[self.windows_index]['window']

            time.sleep(3)

            if self.task_status:
                logger.info("TRANSFER: TRANSFER LIMIT IS FULL. TASK IS DONE")
                break

            if self.transfer_list[self.windows_index]['transfer_status']:
                logger.info("TRANSFER: WINDOW ID:%s. WINDOW TRANSFER LIMIT IS FULLY", self.transfer_list[self.windows_index]['id'])
                self.count_end += 1
                logger.info("TRANSFER: END COUNT: %s", self.count_end)
                self.windows_index += 1
                logger.info("TRANSFER: WINDOW INDEX UP: %s", self.windows_index)
                continue
            if self.transfer_list[self.windows_index]['resourse_status']:
                logger.info("TRANSFER: WINDOW ID:%s. RESOURSE EMPTY", self.transfer_list[self.windows_index]['id'])
                self.count_end += 1
                logger.info("TRANSFER: END COUNT: %s", self.count_end)
                self.windows_index += 1
                logger.info("TRANSFER: WINDOW INDEX UP: %s", self.windows_index)
                continue
            if self.transfer_list[self.windows_index]['fail_count'] >= 3:
                logger.info("TRANSFER:  WINDOW ID:%s. FAIL COUNT TRIGGER. SKIP WINDOW", self.transfer_list[self.windows_index]['id'])
                self.windows_index += 1
                self.count_end += 1
                logger.info("TRANSFER: WINDOW INDEX UP: %s", self.windows_index)
                continue

            window.window.activate()
            time.sleep(3)

            if self.transfer_list[self.windows_index]['screen_status'] is None:
                print(self.transfer_list[self.windows_index])
                self.game_objects.transfer_step_0(window=window, task=self.transfer_list[self.windows_index])
            else:
                print(self.transfer_list[self.windows_index])
                self.game_objects.transfer_step_3(window=window, task=self.transfer_list[self.windows_index])

            self.task_status = self.transfer_list[self.windows_index]['task_status']
            logger.info("TRANSFER: END COUNT: %s", self.count_end)
            self.windows_index += 1
            logger.info("TRANSFER: WINDOW INDEX UP: %s", self.windows_index)
         #Уведомление что все выполнено
        messagebox.showinfo(title=self.locale.i10n('transfer-msgbsi-task-end-title'), message=self.locale.i10n('transfer-msgbsi-task-end-message'))




    def start_task(self):
        self.task_manager.start_task(task_func=self.transfer_algorithm, on_complete_func=self.end_task, name_service='Transfer Resourse Service')

    def end_task(self):
        pass

    def put_widgets(self):
        image_path = resource_path("app/img/buttons/transfer-on.png")
        self.image = tk.PhotoImage(file=image_path)  # Укажите путь к вашему изображению

         # Создаем кнопку с изображением
        button = tk.Button(self, image=self.image, command=self.choose_param_gather)
        button.grid(row=0, column=0)