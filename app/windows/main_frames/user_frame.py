from tkinter import ttk
from tkinter import Label, SOLID, E, W
from app.config.config_manager import ConfigManager
from app.service.validator_manager import ValidatorManager
from app.service.locale_service import Localization


class UserFrame(ttk.Frame):

    def __init__(self, parent):
        self.frame: ttk.Frame = super().__init__(parent, border=1, relief=SOLID)
        self.app = parent
        self.locale: Localization = self.app.locale
        self.user_config: ConfigManager = self.app.user_config
        self.validator: ValidatorManager = self.app.validator
        self.put_widgets()


    def put_widgets(self):
        exp_date = self.user_config.config.user.expired_time

        self.lbl_username = Label(self, text=f"ID: {self.user_config.config.user.client_id}", justify="left", anchor=W, font=('Arial', 8))
        self.lbl_username.grid(row=0, column=0, sticky=W)

        self.license = Label(self, text=f"{self.locale.i10n('license')}:", justify="left", anchor=E, font=('Arial', 8))
        self.license.grid(row=0, column=1, sticky=E)
        self.license_exp_time = Label(self, text=f"", justify="right", anchor=W, font=('Arial', 8))
        control_exp_time = self.validator.days_until(date_str=exp_date)
        if control_exp_time in [self.locale.i10n('day_until_expired'), self.locale.i10n('day_until_not_active')]:
            self.license_exp_time.config(text=control_exp_time, foreground="red")
        else:
            self.license_exp_time.config(text=control_exp_time, foreground="green")
        self.license_exp_time.grid(row=0, column=2, sticky=W)

        self.lbl_server_status = Label(self, text=self.locale.i10n('user_footer_status_server'), justify="left", anchor=E, font=('Arial', 8))
        self.lbl_server_status.grid(row=0, column=3, sticky=E)

        self.lbl_status = Label(self, text="", justify="right", anchor=W, font=('Arial', 8))
        if self.validator.server_status:
            self.lbl_status.config(text=self.locale.i10n('user_footer_online'), foreground="green")
        else:
            self.lbl_status.config(text=self.locale.i10n('user_footer_offline'), foreground="red")
        self.lbl_status.grid(row=0, column=4, sticky=W)

        self.lbl_online = Label(self, text=f"{self.locale.i10n('user_footer_count')}: {self.validator.online}", justify="right", anchor=W, font=('Arial', 8) )
        self.lbl_online.grid(row=0, column=5, sticky=E, columnspan=3)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=2)
        self.grid_columnconfigure(4, weight=2)
        self.grid_columnconfigure(5, weight=4)

    def update_server_status(self):
        if self.validator.server_status:
            self.lbl_status.config(text=self.locale.i10n('user_footer_online'), foreground="green")
        else:
            self.lbl_status.config(text=self.locale.i10n('user_footer_offline'), foreground="red")

        self.lbl_online.config(text=f"{self.locale.i10n('user_footer_online')}: {self.validator.online}")

    def update_license_status(self):
        exp_date = self.user_config.config.user.expired_time
        control_exp_time = self.validator.days_until(date_str=exp_date)
        if control_exp_time in [self.locale.i10n('day_until_expired'), self.locale.i10n('day_until_not_active')]:
            self.license_exp_time.config(text=control_exp_time, foreground="red")
        else:
            self.license_exp_time.config(text=control_exp_time, foreground="green")
        self.license_exp_time.grid(row=0, column=2, sticky=W)

        self.lbl_online.config(text=f"{self.locale.i10n('user_footer_count')}: {self.validator.online}")

    def update_user_id(self):
        user_id = self.user_config.config.user.client_id
        self.lbl_username.config(text=f"{self.locale.i10n('user_footer_id')}: {user_id}")
