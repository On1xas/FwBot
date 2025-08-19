import pyautogui
import cv2
import random
import numpy as np
import time

from pynput.mouse import Button, Controller
import win32api
import win32con

from app.config.config_manager import ConfigManager
from app.service.task_manager import TaskManager
from app.utils.resourse_path import resource_path
from app.utils.cv import find_template_matches
from app.logging import logger
from pygetwindow import Win32Window

class ClickerManager:
    def __init__(self, user_config: int):
        self.user_config: ConfigManager = user_config
        self.windows_list = []

    def find_button(self, img_path):
        ignored_areas=[]
        # Делаем скриншот экрана
        # screenshot = pyautogui.screenshot(region=(x, y, width, height))(x, y) — координаты верхнего левого угла области, а width и height — ширина и высота области соответственно
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
        logger.info(f"FIND COORD: {coordinates}")

        return coordinates

    def find_element(self, img_path):
        # Делаем скриншот экрана
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Загружаем изображение для поиска
        template = cv2.imread(img_path)

        # Создаем список для хранения найденных координат
        coordinates = set()  # Используем set для уникальности

        # Находим совпадения
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Порог для совпадения
        loc = np.where(result >= threshold)

        for pt in zip(*loc[::-1]):  # меняем местами x и y
            if not any(abs(pt[0] - cx) < 15 and abs(pt[1] - cy) < 15 for cx, cy in coordinates):
                # Преобразуем координаты в int и добавляем в set
                coordinates.add((int(pt[0]), int(pt[1])))

        logger.info(f"FIND ELEMENT COORD: {list(coordinates)}")

        # Вычисляем центр найденных элементов
        center_coordinates = []
        for cx, cy in coordinates:
            center_x = cx + (template.shape[1] // 2)
            center_y = cy + (template.shape[0] // 2)
            center_coordinates.append((center_x, center_y))

        return center_coordinates  # Возвращаем координаты центра

    def proportional_click(self, new_width, new_height, new_window_x, new_window_y, original_click_x, original_click_y):

        original_width = 1297
        original_height = 760
        # original_click_x = 1230
        # original_click_y = 580
        # Рассчитываем относительные координаты кнопки
        relative_x = original_click_x / original_width
        relative_y = original_click_y / original_height

        # Вычисляем абсолютные координаты для нового окна
        new_click_x = int(relative_x * new_width) + new_window_x
        new_click_y = int(relative_y * new_height) + new_window_y

        # Перемещаем курсор и выполняем клик
        pyautogui.click(new_click_x, new_click_y)

        logger.info(f"APP: CLICKER MANAGER: PROPORTIONAL CLICK [X:{new_click_x}, Y:{new_click_y}]")

    def click(self, x, y):
        # pyautogui.moveTo(x, y)
        # pyautogui.click()
        SHIFT_LIST = [-3,-2,-1, 0, 1, 2, 3]
        shift_x = random.choice(SHIFT_LIST)
        shift_y = random.choice(SHIFT_LIST)
        win32api.SetCursorPos((x+shift_x, y+shift_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        logger.info(f"CLICKER MANAGER: CLICK - [X:{x}, Y:{y}]")
#  X = 1141, Y = 205

    def input_numbers(self, numbers):
        # Вводим цифры
        logger.info("CLICKER MANAGER: INPUT: %s", str(numbers))
        pyautogui.write(numbers, interval=0.5)

    def press_backspace(self, times=1):
        # Небольшая пауза перед нажатием клавиши
        time.sleep(0.5)  # Можно настроить время ожидания
        # Нажимаем клавишу Backspace указанное количество раз
        for _ in range(times):
            pyautogui.press('backspace')
            logger.info(f"APP: CLICKER MANAGER: PRESS BUTTON - [BACKSPACE]")
            time.sleep(0.2)

    # Пример использования функции
    # Удалить 3 символа

    def press_ecs(self, times=0):
        # Небольшая пауза перед нажатием клавиши
        time.sleep(0.5)  # Можно настроить время ожидания
        # Нажимаем клавишу Backspace указанное количество раз
        pyautogui.press('esc')
        logger.info(f"APP: CLICKER MANAGER: PRESS BUTTON - [Esc]")

    def click_at_current_position(self):
        # Получаем текущие координаты курсора
        current_x, current_y = pyautogui.position()

        # Делаем клик в текущем положении курсора
        pyautogui.click(current_x, current_y)
        logger.info(f"APP: CLICKER MANAGER: CLICK - [X:{current_x}, Y:{current_y}]")

    # pyautogui.moveTo(70,674) Регион
    def proportion_click_in_window(self, window: Win32Window, target_x: int, target_y: int):

        # Константы для исходных размеров окна
        ORIGINAL_WIDTH = 1296
        ORIGINAL_HEIGHT = 759


        # Активируем окно
        window.activate()
        window_rect = window._rect  # Получаем размер и положение окна

        # Получаем текущие размеры окна
        current_width = window_rect.width
        current_height = window_rect.height

        # Рассчитываем коэффициенты для преобразования координат
        x_ratio = current_width / ORIGINAL_WIDTH
        y_ratio = current_height / ORIGINAL_HEIGHT

        # Преобразуем целевые координаты в абсолютные
        absolute_x = window_rect.left + int(target_x * x_ratio)
        absolute_y = window_rect.top + int(target_y * y_ratio)
        SHIFT_LIST = [-3,-2,-1, 0, 1, 2, 3]
        shift_x = random.choice(SHIFT_LIST)
        shift_y = random.choice(SHIFT_LIST)

        # Делаем клик
        win32api.SetCursorPos((absolute_x+shift_x, absolute_y+shift_y))
        # pyautogui.click(absolute_x, absolute_y, duration=0.3)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

        logger.info(f"APP: CLICKER MANAGER: CLICK - [X:{absolute_x}, Y:{absolute_y}]")


    def proportion_alliance_doubleclick_in_window(self, window: Win32Window, target_x: int, target_y: int):

        # Константы для исходных размеров окна
        ORIGINAL_WIDTH = 1296
        ORIGINAL_HEIGHT = 759


        # Активируем окно
        window.activate()
        window_rect = window._rect  # Получаем размер и положение окна

        # Получаем текущие размеры окна
        current_width = window_rect.width
        current_height = window_rect.height

        # Рассчитываем коэффициенты для преобразования координат
        x_ratio = current_width / ORIGINAL_WIDTH
        y_ratio = current_height / ORIGINAL_HEIGHT

        # Преобразуем целевые координаты в абсолютные
        absolute_x = window_rect.left + int(target_x * x_ratio)
        absolute_y = window_rect.top + int(target_y * y_ratio)
        SHIFT_LIST = [-3,-2,-1, 0, 1, 2, 3]
        shift_x = random.choice(SHIFT_LIST)
        shift_y = random.choice(SHIFT_LIST)

        pyautogui.doubleClick(x=absolute_x, y=absolute_y)

        # # Делаем клик
        # win32api.SetCursorPos((absolute_x+shift_x, absolute_y+shift_y))
        # # pyautogui.click(absolute_x, absolute_y, duration=0.3)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        # time.sleep(0.2)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

        logger.info(f"APP: CLICKER MANAGER: CLICK - [X:{absolute_x}, Y:{absolute_y}]")

    def proportion_move_cursor_in_window(self, window: Win32Window, target_x: int, target_y: int):

        # Константы для исходных размеров окна
        ORIGINAL_WIDTH = 1296
        ORIGINAL_HEIGHT = 759

        # Активируем окно
        window.activate()
        window_rect = window._rect  # Получаем размер и положение окна

        # Получаем текущие размеры окна
        current_width = window_rect.width
        current_height = window_rect.height

        # Рассчитываем коэффициенты для преобразования координат
        x_ratio = current_width / ORIGINAL_WIDTH
        y_ratio = current_height / ORIGINAL_HEIGHT

        # Преобразуем целевые координаты в абсолютные
        absolute_x = window_rect.left + int(target_x * x_ratio)
        absolute_y = window_rect.top + int(target_y * y_ratio)

        # Делаем клик
        pyautogui.moveTo(x=target_x, y=target_y)

        logger.info(f"APP: CLICKER MANAGER: MOVE CURSOR TO - [X:{absolute_x}, Y:{absolute_y}]")


    def scroll(self, target):
        pyautogui.scroll(clicks=target)
        logger.info("APP: CLICKER MANAGER: SCROLL AMOUNT: %s", target)


    def back_in_main_screen(self, task_manager: TaskManager):
        # НЕАКТУАЛЬНО
        time.sleep(2)
        logger.info(f"APP: CLICKER MANAGER: CLICK - CONTROL MAIN SCREEN")
        path_region = resource_path(relative_path="app\\img\\game_button\\check_shelter.png")
        path_shelter = resource_path(relative_path="app\\img\\game_button\\region_button.png")

        while not task_manager.stop_event.is_set():
            coord_region = find_template_matches(path_region)
            time.sleep(1)
            if coord_region:
                logger.info(f"APP: CLICKER MANAGER: REGION IN ACTION")
                break
            coord_shelter = find_template_matches(path_shelter)
            time.sleep(1)
            if coord_shelter:
                logger.info(f"APP: CLICKER MANAGER: SHELTER IN ACTION")
                break

            self.press_ecs()
            time.sleep(6)



    def moving_screen_to_baricades(self, window: Win32Window):
        x, y, width, height = window.left, window.top, window.width, window.height
        logger.info(f"APP: CLICKER MANAGER: MOVING SCREEN TO BARICADES]")
        # Вычисляем центр окна
        center_x = x + width // 2
        center_y = y + height // 2

        # Перемещаем курсор в центр окна
        pyautogui.moveTo(center_x, center_y, duration=0.3)
        time.sleep(0.5)
        pyautogui.mouseDown()
        time.sleep(0.2)
        pyautogui.moveTo(x=180, y=210, duration=1)
        pyautogui.mouseUp()
        time.sleep(0.5)

    def scroll_down(self):
        pyautogui.scroll(-2)