import cv2
import numpy as np
import time
import pyautogui

# Путь к изображению-шаблону
template_image_path = 'D:\\DDBot\\app\\utils\\wpric.png'  # замените на путь к вашему шаблону
# Функция для создания скриншота
def take_screenshot():
    screenshot = pyautogui.screenshot()
    # Преобразуем скриншот в формат OpenCV
    screenshot_np = np.array(screenshot)
    # Конвертируем цветовой формат из RGB в BGR
    return cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

# Преобразуем изображения в оттенки серого
def load_and_convert_images():
    main_image = take_screenshot()  # Делаем скриншот
    if main_image is None:
        print("Ошибка: Не удалось создать скриншот.")
        return None, None, None

    template_image = cv2.imread(template_image_path)
    if template_image is None:
        print(f"Ошибка: Не удалось загрузить шаблон по пути: {template_image_path}")
        return None, None, None

    main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
    return main_image, main_gray, template_gray

# Функция для поиска совпадений
def find_matches(main_gray, template_gray):
    h, w = template_gray.shape
    result = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    yloc, xloc = np.where(result >= threshold)

    return xloc, yloc, w, h

# Основной цикл
while True:
    main_image, main_gray, template_gray = load_and_convert_images()
    if main_image is None or template_gray is None:
        break  # Выход из цикла, если произошла ошибка

    xloc, yloc, w, h = find_matches(main_gray, template_gray)

    if len(xloc) == 0:
        print("Совпадений не найдено.")
    else:
        matches = []
        for (x, y) in zip(xloc, yloc):
            matches.append(f'Найдено совпадение в координатах: X={x}, Y={y}')
            # Рисуем прямоугольник вокруг совпадения
            cv2.rectangle(main_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Выводим все найденные совпадения
        print("\n".join(matches))

    # Показываем изображение с отмеченными совпадениями
    # cv2.imshow('Matches', main_image)

    # Ждем 5 секунд перед следующей итерацией
    time.sleep(5)

    # Закрываем окно при нажатии клавиши
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break