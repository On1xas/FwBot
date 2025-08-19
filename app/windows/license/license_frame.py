from tkinter import ttk
from tkinter import Label, Entry, Button, SOLID, EW, NSEW, W, E, NS, NW, N, S, SE, NE, SW, PhotoImage, messagebox

from app.service.clicker_manager import ClickerManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager
from app.service.validator_manager import ValidatorManager
from app.service.locale_service import Localization
from app.utils.resourse_path import resource_path
from app.logging import logger

class LicenseMainFrame(ttk.Frame):
    def __init__(self, parent):
        self.frame: ttk.Frame = super().__init__(parent, padding=(3,3), border=2, borderwidth=3, relief=SOLID)
        self.app = parent
        self.task_manager: TaskManager = self.app.task_manager
        self.user_config: ConfigManager = self.app.user_config
        self.clicker_manager: ClickerManager = self.app.clicker_manager
        self.validator: ValidatorManager = self.app.validator
        self.locale: Localization = self.app.locale
        self.windows_manager = self.app.windows_manager
        self.put_shelters_frame()
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=3)

    def put_shelters_frame(self):
        self.label_id = Label(self, text="Client ID: ", width=11, anchor='center', justify='left')
        self.label_key = Label(self, text="License KEY: ", width=11, anchor='center', justify='left')
        self.label_exp_date = Label(self, text=self.locale.i10n(message_id='license-lbl-exp-date', exp_date=self.expire_time()))

        self.entry_id = Entry(self, justify='left',)
        self.entry_id.insert(0, str(self.user_config.config.user.client_id))
        self.entry_key = Entry(self, justify='left', show="*")
        self.entry_key.insert(0, str(self.user_config.config.user.token))


        good_img_path = resource_path('app\\img\\buttons\\good.png')
        edit_img_path = resource_path('app\\img\\buttons\\edit.png')

        self.good_img = PhotoImage(file=good_img_path)
        self.edit_img = PhotoImage(file=edit_img_path)

        self.button_id = Button(self, image=self.good_img, command=self.get_entry_client_id)
        self.button_key = Button(self, image=self.good_img, command=self.get_entry_token)
        self.button_activate = Button(self, text=self.locale.i10n('license-btn-activate'), command=self.activte_licanse)
        self.button_connect_to_server = Button(self, text=self.locale.i10n('license-btn-connect-to-server'), command=self.connect_to_server)

        self.label_id.grid(row=0, column=0, sticky=(S, E), pady=5)
        self.label_key.grid(row=1, column=0, sticky=(N, E), pady=5)
        self.label_exp_date.grid(row=3, columnspan=3, sticky=EW, pady=7)

        self.entry_id.grid(row=0, column=1, sticky=(W,E,S), pady=5)
        self.entry_key.grid(row=1, column=1, sticky=(N,E,W), pady=5)

        self.button_activate.grid(row=2, column=1, sticky=(N,E,W))

        if self.user_config.config.user.client_id != 0:
            self.entry_id.config(state="readonly")
            self.button_id['image'] = self.edit_img
        else:
            self.entry_id.config(state="normal")
            self.button_id['image'] = self.good_img
        self.button_id.grid(row=0, column=2, sticky=(S, W), padx=2, pady=5)

        if self.user_config.config.user.token != "":
            self.entry_key.config(state="readonly")
            self.button_key['image'] = self.edit_img
        else:
            self.entry_key.config(state="normal")
            self.button_key['image'] = self.good_img
        self.button_key.grid(row=1, column=2, sticky=(N, W), padx=2, pady=5)


        if self.validator.server_status:
            self.button_connect_to_server.config(state='disabled')
        else:
            self.button_connect_to_server.config(state='normal')
        self.button_connect_to_server.grid(row=4, columnspan=3, padx=3, pady=3)




    def get_entry_token(self):
        self.entry_key_state: str = self.entry_key.cget("state").__str__()
        if self.entry_key_state == "normal":
            self.entry_key_value = self.entry_key.get()
            if self.entry_key_value:
                self.entry_key.config(state="readonly")
                self.button_key['image'] = self.edit_img
                logger.info(f"APP: LICENSE FRAME: TOKEN ENTRY - SAVE ENTRY")
                self.user_config.update_token(token=self.entry_key_value)
            else:
                messagebox.showwarning(title=self.locale.i10n('license-msbsw-no-data-error-title'), message=self.locale.i10n('license-msbsw-no-data-error-message'))
                logger.error(f"APP: LICENSE FRAME: TOKEN ENTRY - UNCORRECT ENTRY DATA {self.entry_key_value}")

        if self.entry_key_state == "readonly":
            self.entry_key.config(state="normal")
            self.button_key['image'] = self.good_img
            logger.info(f"APP: LICENSE FRAME: TOKEN ENTRY - EDIT ENTRY")

    def get_entry_client_id(self):
        self.entry_state: str = self.entry_id.cget("state").__str__()
        if self.entry_state == "normal":
            self.entry_value = self.entry_id.get()
            if self.entry_value.isdigit():
                self.entry_id.config(state="readonly")
                self.button_id['image'] = self.edit_img
                logger.info(f"APP: LICENSE FRAME: CLIEND ID ENTRY - SAVE ENTRY")
                self.user_config.update_client_id(client_id=int(self.entry_value))
            else:
                messagebox.showwarning(title=self.locale.i10n('license-msbsw-data-error-title'), message=self.locale.i10n('license-msbsw-data-error-message'))
                logger.error(f"APP: LICENSE FRAME: CLIEND ID ENTRY - UNCORRECT ENTRY DATA {self.entry_value}")

        if self.entry_state == "readonly":
            self.entry_id.config(state="normal")
            self.button_id['image'] = self.good_img
            logger.info(f"APP: LICENSE FRAME: CLIEND ID ENTRY - EDIT ENTRY")


    def expire_time(self):
        date = self.user_config.config.user.expired_time

        if date != "":
            return date

    def activte_licanse(self):
        try:
            result = self.validator.auth()
        except Exception as e:
            print(e)
            return
        if result['status'] == "Fail":
            self.app.validate = False
            self.validator.server_status = True
            self.app.user_frame.update_server_status()
            self.user_config.update_exp_time(time="")
            self.app.render(frame=self.app.render_license_frame)
            self.app.user_frame.update_license_status()
            messagebox.showerror(title=self.locale.i10n('license-msbse-active-lic-error-title'), message=f"{result['error']}")
        else:
                # Сохранить время окончания в конфиг
            self.user_config.update_exp_time(time=result['exp_time'])
            self.app.validate = True
            self.validator.server_status = True
            self.app.user_frame.update_user_id()
            self.app.user_frame.update_server_status()
            self.app.user_frame.update_license_status()
            self.label_exp_date.config(text=self.locale.i10n(message_id='license-lbl-exp-date', exp_date=result['exp_time']))
            self.app.render(frame=self.app.render_shelters_frame)

    def connect_to_server(self):
        result = self.validator.auth()
        if result['error'] == "" and result['status'] == "Authorize":
            logger.info(msg="APP: ******USER AUTORIZE*****")
            self.app.validate = True
            self.validator.server_status = True
            self.app.user_frame.update_server_status()
            self.app.user_frame.update_license_status()
            self.user_config.config.user.expired_time = result['exp_time']
            self.app.render(frame=self.app.render_shelters_frame)
        elif result['error'] == "Connection Error" and result['status'] == "Fail":
            self.validator.server_status = False
            self.app.user_frame.update_server_status()
            messagebox.showinfo(title=self.locale.i10n('license-msbsi-serv-error-title'), message=self.locale.i10n('license-msbsi-serv-error-message'))

        else:
            self.validator.server_status = True
            self.app.user_frame.update_server_status()
            messagebox.showinfo(title=self.locale.i10n('license-msbsi-serv-answ-title'), message=self.locale.i10n('license-msbsi-serv-answ-message'))
        self.app.user_frame.update_server_status()
        self.app.user_frame.update_license_status()