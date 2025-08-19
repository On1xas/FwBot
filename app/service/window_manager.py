import time
from pygetwindow import Win32Window
import pyautogui
import pygetwindow as gw
from tkinter import messagebox
from app.logging import logger
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager

class Window():
    def __init__(self, id, window):
        self.id = id
        self.window:Win32Window = window

    def get_id(self):
        return self.id

    def get_window(self):
        return self.window

    def close(self):
        logger.info(f"APP: WINDOW_MANAGER: CLOSE - SCREEN ID: {self.id}")
        self.window.close()

    def resize(self, x: int, y: int):
        logger.info(f"APP: WINDOW_MANAGER: RESIZE - SCREEN ID: {self.id}, [W: {self.window.width}, H: {self.window.height}] TO [W:{x}, H:{y}]")
        self.window.resize(self.window.width-(self.window.width*2), self.window.height-(self.window.height*2))
        time.sleep(0.3)
        self.window.resize(x,y)
        print(f"x:{self.window.width} y:{self.window.height}")
        time.sleep(0.3)

class WindowManager():
    def __init__(self,app, user_config, task_manager: TaskManager):
        self.app = app
        self.user_config: ConfigManager = user_config
        self.task_manager: TaskManager = task_manager
        self.windows_list = []


    def move_window(self, window_obj: Window, x,y):
        logger.info(f"APP: WINDOW_MANAGER: MOVE - SCREEN ID: {window_obj.id}, MOVE TO X:{x}, Y:{y}")
        pyautogui.moveTo(window_obj.window.left+15, window_obj.window.top+5)
        time.sleep(0.3)
        pyautogui.mouseDown()
        time.sleep(0.3)
        pyautogui.moveTo(x,y,duration=0.5)
        time.sleep(0.3)
        pyautogui.mouseUp()
        time.sleep(0.3)

    def move_all_windows(self):

        if not self.windows_list:
            logger.warn(f"APP: WINDOW MANAGER: WINDOW UNDEFIENED")
        else:
            logger.info(f"APP: WINDOW MANAGER: MOVE SCREEN STARTED")
            # Определяем начальные координаты для размещения
            start_x =1
            start_y = 1
            window_width = self.user_config.config.alliance_config.size_window_x
            # Добавка +40 т.к верхний бар окна не входит в размер окна
            window_height = self.user_config.config.alliance_config.size_window_y+40
            # Задайте ширину и высоту окон для сетки
            padding = 3  # Отступ между окнами
            # Перемещаем каждое окно в сетку
            for i, window in enumerate(self.windows_list):
                if not self.task_manager.stop_event.is_set():
                    window_obj: Window = window
                    window: Win32Window = window_obj.window
                    # Активируем окно
                    window.activate()
                    # Ждем, чтобы окно стало активным
                    time.sleep(0.1)
                    # Получаем координаты для размещения
                    x = start_x + (i % (1920 // window_width)) * (window_width + padding)
                    y = start_y + (i // (1920 // window_width)) * (window_height + padding)
                    # Перемещаем мышь на верхнюю панель окна
                    logger.info(f"APP: WINDOW MANAGER: SCREEN ID - {window_obj.id}, MOVE TO X:{x}, Y:{y}")
                    self.move_window(window_obj=window_obj, x=x, y=y)
                else:
                    logger.info("APP: WINDOW MANAGER: MOVE SCREEN - INTERAPTED")
                    break
            else:
                messagebox.showinfo(title="", message="Расстановка окон завершена")
                logger.info("APP: WINDOW MANAGER: MOVE SCREEN - COMPLETED")



    def init_multi_windows(self):
        self.windows_list.clear()
        window_title = "Fate War"
        windows = gw.getWindowsWithTitle(window_title)
        print(windows)
        if windows:
            for id, window in enumerate(windows, start=1):
                window: Win32Window = window
                time.sleep(1)
                self.windows_list.append(Window(id=id, window=window))

            for win in self.windows_list:
                win: Window
                win.resize(x=1280, y=720)
                time.sleep(2)

        else:
            logger.warning("APP: WINDOW MANAGER: WINDOW UNDEFIENED")
