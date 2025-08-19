
import time
from tkinter import ttk
import tkinter as tk
from tkinter import SOLID, EW, messagebox
from app.utils.resourse_path import resource_path

from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager
from app.service.window_manager import WindowManager, Window
from app.service.game_object_service_OLD import GameObjectService
from app.service.locale_service import Localization
from app.logging import logger

from app.utils.cv import find_template_matches

class ShelterHealerFrame(ttk.Frame):
    def __init__(self, parent, config, task_manager, clicker_manager, windows_manager, game_objects, locale):
        super().__init__(parent, padding=(1,1), border=1, borderwidth=1, relief=SOLID)
        self.user_config: ConfigManager = config
        self.task_manager: TaskManager = task_manager
        self.clicker_manager: ClickerManager = clicker_manager
        self.windows_manager: WindowManager = windows_manager
        self.game_objects: GameObjectService = game_objects
        self.locale: Localization = locale
        self.heal_data = dict()
        self.put_widgets()

    def choose_param_window(self):

        self.choose_window: tk.Toplevel = tk.Toplevel()

        window_width = 300
        window_height = 200

        screen_width = self.choose_window.winfo_screenwidth()
        screen_height = self.choose_window.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.choose_window.title = self.locale.i10n("heal-window-title")
        self.choose_window.geometry(f"{210}x{195}+{x}+{y}")
        self.choose_window.resizable(width=False, height=False)
        self.choose_window.overrideredirect(boolean=True)
        validate_command = self.choose_window.register(self.validate_input)

        self.btn_start = ttk.Button(master=self.choose_window, text=self.locale.i10n("window-start"), command=self.get_data)
        self.btn_cancel = ttk.Button(master=self.choose_window, text=self.locale.i10n("window-cancel"), command=lambda: self.choose_window.destroy())

        lbl_input_unit = tk.Label(master=self.choose_window, text=self.locale.i10n("heal-window-input_unit_label"), justify='center', anchor='center')

        self.path_pex_img = resource_path("app\\windows\\shelter\\healer\\img\\pex.png")
        self.img_pex = tk.PhotoImage(file=self.path_pex_img)
        self.path_svad_img = resource_path("app\\windows\\shelter\\healer\\img\\svad.png")
        self.img_svad = tk.PhotoImage(file=self.path_svad_img)
        self.path_strl_img = resource_path("app\\windows\\shelter\\healer\\img\\strl.png")
        self.img_strl = tk.PhotoImage(file=self.path_strl_img)
        self.path_inj_img = resource_path("app\\windows\\shelter\\healer\\img\\inj.png")
        self.img_inj = tk.PhotoImage(file=self.path_inj_img)
        self.path_all_img = resource_path("app\\windows\\shelter\\healer\\img\\all.png")
        self.img_all = tk.PhotoImage(file=self.path_all_img)

        lbl_pex = tk.Label(master=self.choose_window, image=self.img_pex)
        lbl_vsad = tk.Label(master=self.choose_window, image=self.img_svad)
        lbl_stlk = tk.Label(master=self.choose_window, image=self.img_strl)
        lbl_inj = tk.Label(master=self.choose_window, image=self.img_inj)
        lbl_all = tk.Label(master=self.choose_window, image=self.img_all)

        self.path_select_img = resource_path("app\\windows\\shelter\\healer\\img\\select.png")
        self.path_unselect_img = resource_path("app\\windows\\shelter\\healer\\img\\unselect.png")

        self.var_count_unit = tk.IntVar()
        self.var_pex = tk.BooleanVar()
        self.var_svad = tk.BooleanVar()
        self.var_stlk = tk.BooleanVar()
        self.var_inj = tk.BooleanVar()
        self.var_all = tk.BooleanVar()

        self.img_select = tk.PhotoImage(file=self.path_select_img)
        self.img_unselect = tk.PhotoImage(file=self.path_unselect_img, width=30, height=30)

        self.chckbtn_pex = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_pex,
                                          borderwidth=0)
        self.chckbtn_vsad = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_svad,
                                          borderwidth=0)
        self.chckbtn_stlk = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_stlk,
                                          borderwidth=0)
        self.chckbtn_inj = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_inj,
                                          borderwidth=0)
        self.chckbtn_all = tk.Checkbutton(master=self.choose_window,
                                          image=self.img_unselect,
                                          selectimage=self.img_select,
                                          indicatoron=False,
                                          bg=self.choose_window.cget('bg'),
                                          selectcolor=self.choose_window.cget('bg'),
                                          variable=self.var_all,
                                          borderwidth=0,
                                          command=self.update_all_chckbox
                                        )

        lbl_input_count = tk.Label(master=self.choose_window, text=self.locale.i10n("heal-window-input-count-label"), justify='center', anchor='center')
        self.inpt_btn = tk.Entry(master=self.choose_window, justify='center', validate='key', validatecommand=(validate_command, '%S'))

        lbl_input_unit.grid(row=0,column=0, columnspan=5, sticky=EW)

        lbl_pex.grid(row=1,column=0, padx=1, pady=1, sticky=EW)
        lbl_vsad.grid(row=1,column=1, padx=1, pady=1, sticky=EW)
        lbl_stlk.grid(row=1,column=2, padx=1, pady=1, sticky=EW)
        lbl_inj.grid(row=1,column=3, padx=1, pady=1, sticky=EW)
        lbl_all.grid(row=1,column=4, padx=1, pady=1, sticky=EW)

        self.chckbtn_pex.grid(row=2,column=0, padx=2, pady=1, sticky=EW)
        self.chckbtn_vsad.grid(row=2,column=1, padx=2, pady=1, sticky=EW)
        self.chckbtn_stlk.grid(row=2,column=2, padx=2, pady=1, sticky=EW)
        self.chckbtn_inj.grid(row=2,column=3, padx=2, pady=1, sticky=EW)
        self.chckbtn_all .grid(row=2,column=4, padx=2, pady=1, sticky=EW)

        lbl_input_count.grid(row=3,column=0, columnspan=5, padx=5, pady=5, sticky=EW)
        self.inpt_btn.grid(row=4,column=0, columnspan=5, padx=5, pady=5)

        self.btn_start.grid(row=5,column=0, columnspan=2, padx=5)
        self.btn_cancel.grid(row=5,column=3, columnspan=2, padx=5)

    def validate_input(self, char: str):
        return char.isdigit()


    def get_data(self):
        data = {
            "pex": self.var_pex.get(),
            "vsad": self.var_svad.get(),
            "strl": self.var_stlk.get(),
            "inj": self.var_inj.get(),
            "count_unit": self.inpt_btn.get()
            }
        if self.inpt_btn.get() == "":
            data['count_unit'] = 0
        if any([data['inj'], data['pex'], data['vsad'], data['strl']]):
            pass
        else:
            messagebox.showerror(title=self.locale.i10n("heal-showerror-title"), message=self.locale.i10n("heal-showerror-message-choose-troops"))
            return

        if int(data['count_unit']) <= 0:
            messagebox.showerror(title=self.locale.i10n("heal-showerror-title"), message=self.locale.i10n("heal-showerror-message-count-troops"))
            return


        self.heal_data = data
        self.choose_window.destroy()
        # МЕСТО ЗАПУСКА THREAD
        self.start_task()
        print("task started")


    def update_all_chckbox(self):
        if self.var_all.get():
            self.var_inj.set(value=True)
            self.var_pex.set(value=True)
            self.var_svad.set(value=True)
            self.var_stlk.set(value=True)
        else:
            self.var_inj.set(value=False)
            self.var_pex.set(value=False)
            self.var_svad.set(value=False)
            self.var_stlk.set(value=False)

    def check_shelter(self, window):
        path_region_btn = resource_path(relative_path="app\\img\\game_button\\region_button.png")
        if self.clicker_manager.find_element(path_region_btn):
            print("Я В УБЕЖИЩЕ")
            return True
        print("----- Я НЕ В УБЕЖИЩЕ----")
        return False

    def check_hospital(self):
        pass

    def healer(self):
        self.windows_manager.init_multi_windows()
        window: Window = self.windows_manager.windows_list[0]
        if not self.task_manager.stop_event.is_set():
            window: Window = window
            window.window.moveTo(newLeft=10,newTop=10)
            time.sleep(1)
            logger.info(msg="HEALER: WINDOW MOVED TO [10,10].")
        window.window.activate()
        time.sleep(3)

        self.game_objects.healer(task=self.heal_data)

        messagebox.showinfo(title=self.locale.i10n('heal-task-complete-title'), message=self.locale.i10n('heal-task-complete-message'))


    def healer_new(self):

        # Инициализирую рабочее окно
        self.windows_manager.init_windows_without_login()
        window: Window = self.windows_manager.windows_list[0]
        window.window.activate()
        time.sleep(5)
        while not self.task_manager.stop_event.is_set():

            STATUS_SHELTER = False
            STATUS_HOSPITAL = False
            coordinate_hospital = None
            # Проверка на убежище
            while not STATUS_SHELTER and not STATUS_HOSPITAL or not self.task_manager.stop_event.is_set():
                if self.check_shelter(window=window):
                    STATUS_SHELTER = True
                    # Проверка видит ли больницу
                    coordinate_hospital = self.check_hospital()
                    if coordinate_hospital is None:
                        print("Не вижу больницу")
                        time.sleep(5)
                        continue
                    else:
                        STATUS_HOSPITAL = True
                        break
                else:
                    self.clicker_manager.proportional_click(
                    new_width=window.window.width,
                    new_height=window.window.height,
                    new_window_x=window.window.left,
                    new_window_y=window.window.top,
                    original_click_x=70,
                    original_click_y=674)
                    time.sleep(5)
                    continue
                time.sleep(1)

            # Цикл лечения
            while not self.task_manager.stop_event.is_set():
                # Кликаем на иконку лечения
                self.clicker_manager.click(x=coordinate_hospital[0], y=coordinate_hospital[1])
                time.sleep(1)
                # Кликаем на стрелочку вниз чтоб сбросить количесвто войск лечения
                self.clicker_manager.proportion_click_in_window(window=window.window, target_x=1200, target_y=500)
                time.sleep(1)
                # Смещаем курсор на ввод количесва юнитов первой строки
                self.clicker_manager.proportion_click_in_window(window=window.window, target_x=1135, target_y=200)
                time.sleep(0.3)
                # Второй клик в тоже самое место
                self.clicker_manager.click_at_current_position()
                time.sleep(0.3)
                # Удаляем на всякий случай войска
                self.clicker_manager.press_backspace(8)
                # Вводим количество войск из self.heal_data['count_unit']
                self.clicker_manager.input_numbers(self.heal_data['count_unit'])
                time.sleep(1)
                # Клик на кнопку лечить
                self.clicker_manager.proportion_click_in_window(window=window.window, target_x=1040, target_y=645)
                time.sleep(1)
                # Клик по ручке
                self.clicker_manager.click(x=coordinate_hospital[0], y=coordinate_hospital[1])
                time.sleep(1)
                # Проверка есть на изображении шприц

                while not self.task_manager.stop_event.is_set():
                    path_wpric = resource_path(relative_path="app\\img\\game_button\\wpric.png")
                    if find_template_matches(path_wpric):
                        time.sleep(5)
                        print("Жду пока закончится шприц")
                        continue
                    else:
                        print("Шприц закончился")
                        break

                # Клик по вылеченым войскам
                self.clicker_manager.click(x=coordinate_hospital[0], y=coordinate_hospital[1])
                time.sleep(1)
                break


    def start_task(self):
        self.task_manager.start_task(task_func=self.healer, on_complete_func=self.end_task, name_service='Healer Service')

    def end_task(self):
        pass


    def put_widgets(self):
        image_path = resource_path("app/img/buttons/healer_on.png")
        self.image = tk.PhotoImage(file=image_path)  # Укажите путь к вашему изображениюВД

         # Создаем кнопку с изображением
        button = tk.Button(self, image=self.image, command=self.choose_param_window)
        button.grid(row=0, column=0)
