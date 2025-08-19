from tkinter import ttk
from tkinter import SOLID
from app.service.locale_service import Localization
import webbrowser


class FooterFrame(ttk.Frame):

    def __init__(self, parent):
        self.frame: ttk.Frame = super().__init__(parent, border=1, relief=SOLID)
        self.app = parent
        self.locale: Localization = self.app.locale
        self.put_widgets()

    def on_link_click(self, event):
        # Вставьте сюда ссылку на вашу группу в Telegram
        telegram_group_link = "https://t.me/+w1Y7gs4FfFQyMzIy"  # Замените на реальную ссылку
        webbrowser.open(telegram_group_link)

    def put_widgets(self):
        self.link_label = ttk.Label(self, text=self.locale.i10n('footer_text'), foreground="blue", cursor="hand2")
        self.link_label.grid(row=0, column=0)
        self.link_label.bind("<Button-1>", self.on_link_click)
        self.grid_columnconfigure(0, weight=1)  # Для первой колонки
