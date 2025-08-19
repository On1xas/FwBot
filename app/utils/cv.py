import cv2
import numpy as np
import pyautogui
import time

# from resourse_path import resource_path

template_image_path = 'D:\\DDBot\\app\\utils\\wpric.png'  # замените на путь к вашему шаблону
# Функция для создания скриншота
# Функция для создания скриншота
def take_screenshot():
    screenshot = pyautogui.screenshot()
    # Преобразуем скриншот в формат OpenCV
    screenshot_np = np.array(screenshot)
    # Конвертируем цветовой формат из RGB в BGR
    return cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

# Функция для поиска совпадений по шаблону
def find_template_matches(template_image_path, threshold= 0.8, region = None):
    main_image = take_screenshot()  # Делаем скриншот
    if main_image is None:
        return []

    template_image = cv2.imread(template_image_path)
    if template_image is None:
        return []

    main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    h, w = template_gray.shape
    result = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = threshold
    yloc, xloc = np.where(result >= threshold)

    # Если совпадений нет, возвращаем пустой список
    if len(xloc) == 0:
        return []

    # Создаем список кортежей (x, y) для центров совпадений
    matches = [(int(x + w // 2),int(y + h // 2)) for (x, y) in zip(xloc, yloc)]
    return matches

def find_template_matches_color(template_image_path, threshold=0.8):
    main_image = take_screenshot()  # Делаем скриншот
    if main_image is None:
        return []

    template_image = cv2.imread(template_image_path)
    if template_image is None:
        return []

    # Преобразуем изображения в цветовое пространство HSV
    main_hsv = cv2.cvtColor(main_image, cv2.COLOR_BGR2HSV)
    template_hsv = cv2.cvtColor(template_image, cv2.COLOR_BGR2HSV)

    h, w = template_hsv.shape[:2]
    result = cv2.matchTemplate(main_hsv, template_hsv, cv2.TM_CCOEFF_NORMED)

    # Получаем координаты, где совпадение выше порога
    yloc, xloc = np.where(result >= threshold)

    # Если совпадений нет, возвращаем пустой список
    if len(xloc) == 0:
        return []

    # Создаем список кортежей (x, y) для центров совпадений
    matches = [(int(x + w // 2), int(y + h // 2)) for (x, y) in zip(xloc, yloc)]
    return matches
# while True:
#     res = find_template_matches(template_image_path)
#     print(res)
#     time.sleep(5)


def preprocess_image(image):
    # Преобразуем в серый цвет
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Применяем размытие для уменьшения шума
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return blurred

def find_template_simple(template_image_path, threshold=0.8):
    # Загружаем основное изображение (например, скриншот)
    main_image = take_screenshot()  # Сделать скриншот
    if main_image is None:
        return []

    # Загружаем шаблон
    template_image = cv2.imread(template_image_path)
    if template_image is None:
        return []

    # Получаем размеры шаблона
    h, w = template_image.shape[:2]

    # Выполняем шаблонное совпадение
    result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)
    yloc, xloc = np.where(result >= threshold)

    # Если совпадений нет, возвращаем пустой список
    if len(xloc) == 0:
        return []

    # Создаем список кортежей (x, y) для центров совпадений
    matches = [(int(x + w // 2), int(y + h // 2)) for (x, y) in zip(xloc, yloc)]
    return matches

def filter_coordinates(coords, threshold=20):
    # Сортируем координаты
    coords.sort()

    filtered = []

    for coord in coords:
        # Проверяем, есть ли уже отфильтрованная координата, которая близка к текущей
        is_close = any(
            abs(coord[0] - f_coord[0]) < threshold and abs(coord[1] - f_coord[1]) < threshold
            for f_coord in filtered
        )

        # Если нет близкой координаты, добавляем в отфильтрованный список
        if not is_close:
            filtered.append(coord)

    return filtered



if __name__ == "__main__":
    cex_build = resource_path(relative_path="app\\img\\game_button\\cex_build.png")
    coord_cex_build = find_template_matches_color(cex_build)
    print(coord_cex_build)