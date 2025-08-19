import pygetwindow as gw
import pyautogui
import time


def minimize_size_window():
    window_title = "Doomsday: Last Survivors"
    # Получаем окно
    windows = gw.getWindowsWithTitle(window_title)
    # 1280x720

    if not windows:
        print("Окно с таким названием не найдено.")
    else:
        for i, window in enumerate(windows, start=1):
            # Вычисляем координаты
            x1 = window.right - 75
            y1 = window.top+6
            x2 = window.right - 55
            y2 = window.top + 15

            # Клик на (window.right - 25, window.top)
            pyautogui.rightClick(x1, y1)
            time.sleep(0.5)  # Ждем полсекунды

            # Клик на (window.right - 25, window.top - 25)
            pyautogui.leftClick(x2, y2)
            time.sleep(0.5)  # Ждем полсекунды

            print(f"Окнo {i} уменьшено")

def move_all_windows():

    # Название окон
    window_title = "Doomsday: Last Survivors"

    # Получаем список всех окон с заданным названием
    windows = gw.getWindowsWithTitle(window_title)

    if not windows:
        print("Окно с таким названием не найдено.")
    else:
        # Определяем начальные координаты для размещения
        start_x, start_y = 1, 1
        window_width, window_height = 320, 240  # Задайте ширину и высоту окон для сетки
        padding = 3  # Отступ между окнами

        # Перемещаем каждое окно в сетку
        for i, window in enumerate(windows):
            # Активируем окно
            window.activate()

            # Ждем, чтобы окно стало активным
            time.sleep(0.1)

            # Получаем координаты для размещения
            x = start_x + (i % 6) * (window_width + padding)  # 3 окна в ряд
            y = start_y + (i // 6) * (window_height + padding)

            # Перемещаем мышь на верхнюю панель окна
            pyautogui.moveTo(window.left, window.top)

            # Нажимаем и удерживаем левую кнопку мыши
            pyautogui.mouseDown()

            # Перемещаем окно в заданные координаты
            pyautogui.moveTo(x, y)

            # Отпускаем кнопку мыши
            pyautogui.mouseUp()

        print("Окна размещены в сетке.")