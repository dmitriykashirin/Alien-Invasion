import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс для создания пришельца и управления его позицией."""

    def __init__(self, ai):
        """Инициализирует атрибуты экрана, пришельца и класса родителя."""
        super().__init__()
        self.screen = ai.screen
        self.settings = ai.settings

        # Загружает изображение пришельца.
        self.image = pygame.image.load('images/пришелец.bmp')
        self.rect = self.image.get_rect()

        # Задаёт пришельцу начальную позицию у верхнего левого края экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохраняет горизонтальное положение пришельца в десятичном формате.
        self.x = float(self.rect.x)

    def check_edge(self):
        """Возвращает True, если флот дошёл до края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False


    def update(self):
        """Обновляет позицию пришельца."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x