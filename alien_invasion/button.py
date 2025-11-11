import pygame
class Button:
    """Класс, который выводит кнопки на экран игры Alien Invasion."""

    def __init__(self, ai):
        """Инициализирует атрибуты кнопки."""
        self.screen = ai.screen
        self.screen_rect = self.screen.get_rect()
        # Загружает изображение кнопки play и создаёт его прямоугольник.
        self.image = pygame.image.load('images/кнопка play.png')
        self.rect = self.image.get_rect()
        # Выравнивает кнопку по центру экрана.
        self.rect.center = self.screen_rect.center


    def blitme(self):
        """Рисует кнопку в текущей позиции."""
        self.screen.blit(self.image, self.rect)

