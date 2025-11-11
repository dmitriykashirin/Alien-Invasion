class Settings:
    """Класс для хранения всех настроек игры 'Alien Invasion'."""

    def __init__(self):
        """Инициализирует постоянные настройки игры."""
        # Параметры экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Настройки корабля.
        self.ship_limit = 2

        # Параметры снаряда.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 15

        # Параметры пришельца.
        self.fleet_drop_speed = 10
        # Коэффициент изменения скорости.
        self.speed_scale = 1.5

        self._increase_speed()

    def _increase_speed(self):
        """Хранит изменяющиеся настройки игры."""
        self.ship_speed = 1.5
        self.bullet_speed = 1
        self.alien_speed = 1.0
        # fleet_direction = 1 - лот движется вправо, если -1 - то влево.
        self.fleet_direction = 1

    def new_speed(self):
        """Изменяет скорость игры."""
        self.ship_speed *= self.speed_scale
        self.bullet_speed *= self.speed_scale
        self.alien_speed *= self.speed_scale

