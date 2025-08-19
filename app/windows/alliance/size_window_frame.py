from tkinter import ttk
from tkinter import Label, Entry, Button, SOLID, EW, E, W, messagebox, DISABLED, NORMAL, CENTER
from app.config.config_manager import ConfigManager
from app.service.locale_service import Localization


dict_size = {
            "320x240(24)": {
                "x": 304,
                "y": 200
                },
            "265x220(30)": {
                "x": 220,
                "y": 160
            }
        }


class ChooseSizeWindow(ttk.Frame):
    def __init__(self, parent, config, locale):
        self.frame: ttk.Frame = super().__init__(parent, padding=(3,3), border=2, borderwidth=3, relief=SOLID)
        self.user_config: ConfigManager = config
        self.locale: Localization = locale
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.put_widgets()



    def get_size(self):

        self.combobox_state: str = self.size_combobox.cget("state").__str__()
        if self.combobox_state == NORMAL:
            choose = self.size_combobox.get()
            x = dict_size[choose]['x']
            y = dict_size[choose]['y']
            self.size_combobox.config(state=DISABLED)
            self.button_save_xy['text'] = self.locale.i10n('button-edit')
            self.user_config.update_size_window(int(x) ,int(y))

        if self.combobox_state == DISABLED:
            self.size_combobox.config(state=NORMAL)
            self.button_save_xy['text'] = self.locale.i10n('button-save')




    def put_widgets(self):

        size_list = [key for key in dict_size.keys()]
        label_XY = Label(self, text=self.locale.i10n('size-window'))
        label_XY.grid(row=0, column=0, columnspan=2, sticky=EW)

        self.size_combobox = ttk.Combobox(self, values=size_list, justify=CENTER)
        self.size_combobox.grid(row=1,column=0, columnspan=2)

        self.button_save_xy = ttk.Button(self, text=self.locale.i10n('button-save'), command=self.get_size)
        if self.user_config.config.alliance_config.size_window_x != 0 and self.user_config.config.alliance_config.size_window_y != 0:
            for key in size_list:
                if self.user_config.config.alliance_config.size_window_x == dict_size[key]['x'] and self.user_config.config.alliance_config.size_window_y == dict_size[key]['y']:
                    self.size_combobox.set(key)
                    self.size_combobox.config(state=DISABLED)
                    self.button_save_xy['text'] = self.locale.i10n('button-edit')
                    break
            else:
                self.button_save_xy['text'] = self.locale.i10n('button-save')

        else:
            self.size_combobox.config(state=NORMAL)
            self.button_save_xy.config(text= self.locale.i10n('button-save'))
        self.button_save_xy.grid(row=3, column=0, columnspan=2, padx=3, pady=3, sticky=EW)
