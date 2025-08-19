from tkinter import filedialog
from tkinter import ttk, SOLID, EW
from app.config.config_manager import ConfigManager
from app.service.locale_service import Localization

class ChooseEXEPathFrame(ttk.Frame):
    def __init__(self, parent, config, locale):
        super().__init__(parent, padding=(3,3), relief=SOLID)
        self.user_config: ConfigManager = config
        self.locale: Localization = locale
        self.grid_columnconfigure(0, weight=1)
        self.put_widgets()

    def get_exe_path(self):
    # Открываем диалоговое окно для выбора файла
        exe_path = filedialog.askopenfilename(
        title=self.locale.i10n('entry-game-filedialog-title'),
        filetypes=[(self.locale.i10n('entry-game-filedialog-filetypes'), "*.exe")])
        if exe_path:
            self.user_config.update_path_exe(exe_path)
            self.exe_lbl['text'] = exe_path
            self.exe_lbl.config(
                font=('Arial', 7),
                foreground="green",
                justify='center',
                anchor='center',
                wraplength=200
            )

        else:
            # Файл не выбран
            pass

    def put_widgets(self):
        self.exe_path = ttk.Button(self, text=self.locale.i10n('entry-game-path-btn'), command=self.get_exe_path)
        self.exe_path.grid(row=1, column=0, sticky=EW)
        if self.user_config.config.alliance_config.path_to_exe:
            if len(self.user_config.config.alliance_config.path_to_exe)>45:
                path = self.user_config.config.alliance_config.path_to_exe[0:30] +"..."
            else:
                path = self.user_config.config.alliance_config.path_to_exe
            self.exe_lbl = ttk.Label(
                self,
                text=path,
                font=('Arial', 7),
                foreground="green",
                justify='center',
                anchor='center',
                wraplength=200)

        else:
            self.exe_lbl = ttk.Label(
                self,
                text=self.locale.i10n('entry-game-path-label'),
                font=('Arial', 7),
                foreground="red",
                justify='center',
                anchor='center'
                )
        self.exe_lbl.grid(row=2,column=0, sticky=EW)