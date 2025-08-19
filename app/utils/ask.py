import tkinter as tk
from app.config import locale

def on_ok(root):
    root.destroy()
    return True

def on_cancel(root):
    root.destroy()
    return False

def askokcancel(title, message):
    # Создаем главное окно
    root = tk.Toplevel()
    root.title(title)

    # Определяем размеры окна
    width = 250
    height = 150

    # Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Вычисляем координаты для центрирования
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Устанавливаем размеры и позицию окна
    root.geometry(f"{width}x{height}+{x}+{y}")
    # Создаем метку с сообщением
    label = tk.Label(root, text=message)
    label.pack(pady=10)

    # Функции для обработки нажатия кнопок


    # Создаем кнопки с локализованным текстом
    ok_button = tk.Button(root, text="OK", command=lambda: on_ok(root))
    ok_button.pack(side=tk.LEFT, padx=20,  pady=5)

    cancel_button = tk.Button(root, text=locale.i10n('cancel'), command=lambda: on_cancel(root))
    cancel_button.pack(side=tk.RIGHT, padx=20, pady=5)
