import tkinter as tk
import sys
import traceback
import requests

# URL сервера, на который будет отправляться лог
LOG_SERVER_URL = "https://your-server.com/log"  # Замените на ваш URL

def log_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # Форматируем сообщение об ошибке
    error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    # Отправляем лог на сервер
    try:
        response = requests.post(LOG_SERVER_URL, json={"error": error_message})
        if response.status_code == 200:
            print("Лог ошибки успешно отправлен на сервер.")
        else:
            print("Ошибка при отправке лога на сервер:", response.status_code)
    except Exception as e:
        print("Не удалось отправить лог на сервер:", e)

# Устанавливаем глобальный обработчик исключений
sys.excepthook = log_exception

def faulty_function():
    # Пример функции, которая вызывает исключение
    raise ValueError("Это пример исключения!")

def run_faulty_function():
    try:
        faulty_function()
    except Exception as e:
        print(f"Произошла ошибка: {e}")