import pyautogui
import cv2
import numpy as np
import time
import sys
import os
from pygetwindow import Win32Window
import pyautogui
import pygetwindow as gw




def input_numbers(numbers):
    # Вводим цифры
    pyautogui.write(numbers, interval=0.5)

def press_backspace(times=1):
    # Небольшая пауза перед нажатием клавиши
    time.sleep(0.5)  # Можно настроить время ожидания
    # Нажимаем клавишу Backspace указанное количество раз
    for _ in range(times):
        pyautogui.press('backspace')
        print('Нажата клавиша Backspace')

# Пример использования функции
  # Удалить 3 символа


def click_at_current_position():
    # Получаем текущие координаты курсора
    current_x, current_y = pyautogui.position()

    # Делаем клик в текущем положении курсора
    pyautogui.click(current_x, current_y)
    print(f'Клик выполнен в ({current_x}, {current_y})')
# pyautogui.moveTo(70,674) Регион
def click_in_window(window: Win32Window, target_x: int, target_y: int):
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
    pyautogui.click(absolute_x, absolute_y)
    print(f'Клик выполнен в ({absolute_x}, {absolute_y})')



        # window.moveTo(1,1)
        # time.sleep(0.5)     # Ждем, чтобы окно успело активироваться
        # time.sleep(0.5)
        # click_in_window(window=window, target_x=1200, target_y=500)
        # time.sleep(0.3)
        # click_in_window(window=window, target_x=1141, target_y=205)
        # click_at_current_position()
        # press_backspace(8)
        # input_numbers("1")
        # time.sleep(0.5)
        # click_in_window(window=window, target_x=1040, target_y=645)
        # time.sleep(0.5)


# Запускаем слушатель
# with mouse.Listener(on_click=on_click) as listener:



if __name__ == "__main__":
    ORIGINAL_WIDTH = 1296
    ORIGINAL_HEIGHT = 759

    window_title = "Doomsday: Last Survivors"
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        for window in windows:
            window: Win32Window = window

            window.resize(window.width-(window.width*2), window.height-(window.height*2))
            window.resize(1296,759)
            print(window.size)
            window.activate()   # Активируем окно

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
            absolute_x = window_rect.left + int(1200 * x_ratio)
            absolute_y = window_rect.top + int(200 * y_ratio)


            screenshot = pyautogui.screenshot(region=(absolute_x, absolute_y, 50, 25))

            screenshot_np = np.array(screenshot)  # Преобразуем в NumPy массив

            # Преобразование цветового пространства (RGB в BGR)
            screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

            # Преобразование в оттенки серого
            gray_image = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

            # Применение порогового преобразования для выделения цифр
            _, thresh = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

            # Поиск контуров
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Обработка каждого контура
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                roi = thresh[y:y+h, x:x+w]  # Извлечение области интереса

                # Здесь можно добавить код для распознавания цифр в roi
                # Например, использовать простое шаблонное сопоставление

                # Для демонстрации: выводим координаты контуров
                print(f"Найдена цифра в области: x={x}, y={y}, w={w}, h={h}")
            cv2.imwrite('output.png', thresh)
            print("Изображение сохранено как output.png")