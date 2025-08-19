import requests
import uuid

from app.config.config_manager import ConfigManager

def get_hw_id():
    # Получаем уникальный идентификатор устройства
    hw_id = str(uuid.getnode())
    return hw_id

def is_validate(config: ConfigManager):
    url = "http://127.0.0.1:5000/api/v1/auth"

    payload = {
        "client_id": config.config.user.client_id,
        "token": config.config.user.token,
        "hwID": get_hw_id()
    }
    try:
        response = requests.post(url, json=payload)
    except ConnectionError as e:
        print("Cервер недоступен")
    if response.status_code == 200:
        resp = response.json()
        if resp['status'] == "Fail":
            print(resp['error'])
            return False
        else:
            print("validate")
            return True
    else:
        return {"error": response.json()}  # Возвращает сообщение об ошибке