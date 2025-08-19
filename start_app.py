import os
import tkinter as tk
from tkinter import messagebox

from app.desktop_app import MyApp
from app.config import config, locale
from app.logging import logger


def start_app():
    pass

def on_close(app: tk.Tk):
    if messagebox.askokcancel(title=locale.i10n('quit'), message=locale.i10n('ask_quit')):
        if os.path.exists("launcher.log"):
            os.remove("launcher.log")
            logger.info(msg=f"APP: launcher.log DELETED")
        app.destroy()
        logger.info(msg=f"APP: WN CLOSE")

if __name__ == "__main__":

    start_app()
    app: MyApp = MyApp(config)
    logger.info(msg=f"APP: READY TO WORK")
    app.protocol("WM_DELETE_WINDOW", lambda: on_close(app))
    app.mainloop()
