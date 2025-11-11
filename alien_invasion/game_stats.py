class GameStats:
    """Хранит статистику игры Alien Invasion."""

    def __init__(self, ai):
        """Инициализирует атрибуты статистики."""
        self.settings = ai.settings
        self.reset_stats()
        # Флаг, отвечающий за продолжение игры.
        self.game_active = False

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ship_left = self.settings.ship_limit