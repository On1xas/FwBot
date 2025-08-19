from tkinter import Label, SOLID, W, E, messagebox
from tkinter import ttk
from app.config.config_manager import ConfigManager
from app.service.locale_service import Localization
from app.logging import logger


class ChooseOpenWindows(ttk.Frame):
    def __init__(self, parent, config, locale):
        super().__init__(parent, padding=(3,3), relief=SOLID)
        self.user_config: ConfigManager = config
        self.locale: Localization = locale
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.put_widgets()

    def get_entry(self):
        self.entry_state: str = self.entry.cget("state").__str__()
        if self.entry_state == "normal":
            self.entry_value = self.entry.get()
            if self.entry_value.isdigit():
                self.entry.config(state="readonly")
                self.button['text'] = self.locale.i10n('button-edit')
                logger.info(f"APP: ALLIANCE FRAME: CHOOSE_OPEN_FRAME - SAVE ENTRY")
                self.user_config.update_count_open_window(count=int(self.entry_value))
            else:
                messagebox.showwarning(title=self.locale.i10n('messagebox-warning-title-error-entry'), message=self.locale.i10n('messagebox-warning-message-error-entry'))
                logger.error(f"APP: ALLIANCE FRAME: CHOOSE_OPEN_FRAME - UNCORRECT ENTRY DATA {self.entry_value}")

        if self.entry_state == "readonly":
            self.entry.config(state="normal")
            self.button['text'] = self.locale.i10n('button-save')
            logger.info(f"APP: ALLIANCE FRAME: CHOOSE_OPEN_FRAME - EDIT ENTRY")




    def put_widgets(self):

        self.label = Label(self, text=self.locale.i10n('menu-count-widnows'))
        self.label.grid(row=0, column=0, sticky=E)

        self.entry = ttk.Entry(self, width=5, justify="center")
        self.entry.insert(0, str(self.user_config.config.alliance_config.count_open_window))
        self.entry.grid(row=0, column=1, sticky=W)

        self.button = ttk.Button(self, command=self.get_entry)
        if self.user_config.config.alliance_config.count_open_window != 0:
            self.entry.config(state="readonly")
            self.button['text'] = self.locale.i10n('button-edit')
        else:
            self.entry.config(state="normal")
            self.button['text'] = self.locale.i10n('button-save')
        self.button.grid(row=1, columnspan=2, padx=6,pady=6)
