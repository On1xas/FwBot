import pygetwindow as gw
import pyautogui
import time
import cv2
import numpy as np

from tkinter import messagebox
from pygetwindow import Win32Window

from app.service.window_manager import Window, WindowManager
from app.service.task_manager import TaskManager
from app.config.config_manager import ConfigManager

from app.logging import logger


class ClickerManager:
    def __init__(self, user_config: ConfigManager):
        self.user_config: ConfigManager = user_config
        # self.window_manager: WindowManager = window_manager
        self.windows_list = []

    def find_button(self, img_path):
        ignored_areas=[]
        # Делаем скриншот экрана
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Загружаем изображение для поиска
        template = cv2.imread(img_path)
        h, w = template.shape[:-1]

        # Создаем список для хранения найденных координат
        coordinates = []

        # Ищем совпадения с разными масштабами
        for scale in np.linspace(0.5, 1.5, 10)[::-1]:  # Изменяем масштаб от 50% до 150%
            resized_template = cv2.resize(template, (int(w * scale), int(h * scale)))
            res_h, res_w = resized_template.shape[:-1]

            # Находим совпадения
            result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8  # Порог для совпадения
            loc = np.where(result >= threshold)

            for pt in zip(*loc[::-1]):  # меняем местами x и y
                # Проверяем, находится ли найденная область в игнорируемых зонах
                if any(abs(pt[0] - ix) < 30 and abs(pt[1] - iy) < 30 for ix, iy in ignored_areas):
                    continue  # Пропускаем, если координаты близки к игнорируемым

                # Добавляем найденные координаты, если они уникальны
                if not any(abs(pt[0] - cx) < 30 and abs(pt[1] - cy) < 30 for cx, cy in coordinates):
                    coordinates.append(pt)
                    # Рисуем прямоугольник вокруг найденного изображения (для отладки)
                    # cv2.rectangle(screenshot, pt, (pt[0] + res_w, pt[1] + res_h), (0, 255, 0), 2)

        # Сохраняем изображение с отмеченными координатами (для отладки)
        # cv2.imwrite('result.png', screenshot)
        logger.info(f"FIND HAND: {coordinates[0]}")

        return coordinates

    def proportional_click(self, new_width, new_height, new_window_x, new_window_y):

        original_width = 1297
        original_height = 760
        original_click_x = 1230
        original_click_y = 580
        # Рассчитываем относительные координаты кнопки
        relative_x = original_click_x / original_width
        relative_y = original_click_y / original_height

        # Вычисляем абсолютные координаты для нового окна
        new_click_x = int(relative_x * new_width) + new_window_x
        new_click_y = int(relative_y * new_height) + new_window_y

        # Перемещаем курсор и выполняем клик
        pyautogui.moveTo(new_click_x, new_click_y)
        pyautogui.click()
        logger.info(f"APP: ALLIANCE FRAME: PROPORTIONAL CLICK [X:{new_click_x}, Y:{new_click_y}]")

    def click(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click()
        logger.info(f"APP: CLICKER MANAGER: Click - ({x}, {y})")
        print()

    def check_region(self):
        if isinstance(self.find_button("check_region.png"), tuple):
            return True
        return False

    def check_shelter(self):
        if isinstance(self.find_button("check_shelter.png"), tuple):
            return True
        return False

    def init_windows_without_login(self):
        self.windows_list = []
        window_title = "Doomsday: Last Survivors"
        windows = gw.getWindowsWithTitle(window_title)
        temp=[]
        if windows:
            for id, window in enumerate(windows, start=1):
                if len(temp) <= self.user_config.config.alliance_config.count_open_window:
                #  windows = windows[0:self.user_config.config.alliance_config.count_open_window]
                    temp.append(Window(id=id, window=window))
                else:
                    window.close()
            for window in temp:
                try:
                    # l,pw = l_pw_list.pop()
                    window: Window = window
                    window.user = None
                    window.pw = None
                    self.windows_list.append(window)
                except IndexError:
                    window.close()

            self.windows_list = self.windows_list
        else:
            logger.warn(f"APP: CLICKER MANAGER: WINDOW UNDEFIENED")

    def move_all_windows(self, task_manager: TaskManager):

        if not self.windows_list:
            logger.warn(f"APP: CLICKER MANAGER: WINDOW UNDEFIENED")
        else:
            logger.info(f"APP: CLICKER MANAGER: MOVE SCREEN STARTED")
            # Определяем начальные координаты для размещения
            start_x =1
            start_y = 1
            window_width = self.user_config.config.alliance_config.size_window_x
            window_height = self.user_config.config.alliance_config.size_window_y+40
            # Задайте ширину и высоту окон для сетки
            padding = 3  # Отступ между окнами
            # Перемещаем каждое окно в сетку
            for i, window in enumerate(self.windows_list):
                if not task_manager.stop_event.is_set():
                    widnow_obj: Window = window
                    window: Win32Window = widnow_obj.window
                    # Активируем окно
                    window.activate()
                    # Ждем, чтобы окно стало активным
                    time.sleep(0.1)
                    # Получаем координаты для размещения
                    x = start_x + (i % (1920 // window_width)) * (window_width + padding)
                    y = start_y + (i // (1920 // window_width)) * (window_height + padding)
                    # Перемещаем мышь на верхнюю панель окна

                    logger.info(f"APP: CLICKER MANAGER: SCREEN ID - {widnow_obj.id}, MOVE TO X:{x}, Y:{y}")
                    pyautogui.moveTo(window.left+15,window.top+5)
                    time.sleep(0.3)
                    pyautogui.mouseDown()
                    time.sleep(0.3)
                    pyautogui.moveTo(x,y,duration=0.5)
                    time.sleep(0.3)
                    pyautogui.mouseUp()
                    # window.move(x, y)
                    time.sleep(0.3)
                else:
                    logger.info(f"APP: CLICKER MANAGER: MOVE SCREEN - INTERAPTED")
                    break
            else:
                messagebox.showinfo(title="", message="Расстановка окон завершена")
                logger.info(f"APP: CLICKER MANAGER: MOVE SCREEN - COMPLETED")
