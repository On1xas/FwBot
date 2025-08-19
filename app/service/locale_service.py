import os
from fluent.runtime import FluentResource, FluentBundle, FluentLocalization, FluentResourceLoader

from app.utils.resourse_path import resource_path

class Localization:
    def __init__(self, locale='ru'):
        self.locale = locale
        self.localization: FluentLocalization = self.load_localization(locale)

        if self.localization is None:
            raise RuntimeError(f"Не удалось загрузить локализацию для языка '{locale}'.")

    def load_localization(self, locale):
        # Определение пути к файлам локализации
        localization_dir = resource_path(relative_path="app\\locale")
        file_path = os.path.join(localization_dir, f'{locale}.ftl')

        if not os.path.exists(file_path):
            print(f"Файл локализации '{file_path}' не найден.")
            return None

        loader = FluentResourceLoader(localization_dir)
        l10n = FluentLocalization(["ru", "en"], [f'{locale}.ftl'], loader)
        return l10n

    def switch_locale(self, new_locale):
        """Переключение на новую локализацию."""
        self.locale = new_locale
        self.localization = self.load_localization(new_locale)

        if self.localization is None:
            raise RuntimeError(f"Не удалось загрузить локализацию для языка '{new_locale}'.")

    def i10n(self, message_id, **kwargs):
        # Перевод сообщения по его идентификатору
        if self.localization is None:
            print("Локализация не загружена.")
            return message_id  # Возвращаем ключ, если локализация не загружена

        message = self.localization.format_value(msg_id=message_id, args=kwargs)
        if message:
            return message
        else:
            print(f"Сообщение с идентификатором '{message_id}' не найдено.")
            return message_id  # Возвращаем ключ, если сообщение не найдено