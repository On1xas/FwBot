class GameState:
    def handle(self):
        pass


class MapState(GameState):
    def handle(self):
        print("На карте. Выполняем действия на карте.")
        # Здесь можно добавить логику для выполнения действий на карте


class AdState(GameState):
    def handle(self):
        print("Реклама. Переходим к кнопке 2.")
        # Логика для нажатия кнопки 2
        self.press_button(2)

    def press_button(self, button):
        print(f"Нажата кнопка {button}")


class MenuState(GameState):
    def handle(self):
        print("Меню открыто. Переходим к кнопке 5.")
        # Логика для нажатия кнопки 5
        self.press_button(5)

    def press_button(self, button):
        print(f"Нажата кнопка {button}")


class ConnectionErrorState(GameState):
    def handle(self):
        print("Ошибка соединения. Переходим к кнопке 4.")
        # Логика для нажатия кнопки 4
        self.press_button(4)

    def press_button(self, button):
        print(f"Нажата кнопка {button}")


class Game:
    def __init__(self):
        self.state = MapState()  # Начальное состояние

    def set_state(self, state):
        self.state = state

    def update(self):
        # Здесь вы можете добавлять логику для определения текущего состояния
        # Например, в зависимости от окна игры или других условий
        # Для примера, будем просто вызывать handle()
        self.state.handle()

        # Пример изменения состояния
        # В реальном приложении это должно основываться на условиях
        # self.set_state(AdState())  # Пример переключения на рекламу
        # self.set_state(MenuState())  # Пример переключения на меню
        # self.set_state(ConnectionErrorState())  # Пример ошибки соединения


# Пример использования
game = Game()

# Основной цикл
while True:
    game.update()
    # Здесь можно добавить задержку или другие условия выхода из цикла
    break  # Уберите это, чтобы цикл работал бесконечно