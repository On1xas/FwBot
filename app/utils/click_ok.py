import pyautogui
import cv2
import numpy as np

import time

def find_button(image_path):
    ignored_areas = []
    # Делаем скриншот экрана
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Загружаем изображение для поиска
    template = cv2.imread(image_path)
    h, w = template.shape[:-1]

    # Создаем список для хранения найденных координат
    coordinates = []

    # Ищем совпадения с разными масштабами
    for scale in np.linspace(0.5, 2.0, 20)[::-1]:  # Изменяем масштаб от 50% до 200%
        resized_template = cv2.resize(template, (int(w * scale), int(h * scale)))
        res_h, res_w = resized_template.shape[:-1]

        # Находим совпадения
        result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9  # Порог для совпадения
        loc = np.where(result >= threshold)

        print(f"Масштаб: {scale}, Найдено совпадений: {len(loc[0])}")

        for pt in zip(*loc[::-1]):  # меняем местами x и y
            # Проверяем, находится ли найденная область в игнорируемых зонах
            if any(abs(pt[0] - ix) < 30 and abs(pt[1] - iy) < 30 for ix, iy in ignored_areas):
                continue  # Пропускаем, если координаты близки к игнорируемым

            # Добавляем найденные координаты, если они уникальны
            if not any(abs(pt[0] - cx) < 30 and abs(pt[1] - cy) < 30 for cx, cy in coordinates):
                coordinates.append(pt)
                # Рисуем прямоугольник вокруг найденного изображения (для отладки)
                cv2.rectangle(screenshot, pt, (pt[0] + res_w, pt[1] + res_h), (0, 255, 0), 2)

    # Сохраняем изображение с отмеченными координатами (для отладки)
    cv2.imwrite('result.png', screenshot)
    print(f"Найденные координаты: {coordinates}")

    return coordinates

def click_button(x,y):
    # Перемещаем мышь и кликаем
    pyautogui.moveTo(x, y)
    pyautogui.click()
    print(f"Клик по кнопке на координатах: ({x}, {y})")