import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Создаёт экземпляры снарядов."""

    def __init__(self, ai):
        """Инициализирует атрибуты Sprite и атрибуты снаряда"""
        super().__init__()
        self.screen = ai.screen
        self.settings = ai.settings
        self.color = self.settings.bullet_color

        # Создание снаряда в позиции 0,0 и назначение правильной позиции.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai.ship.rect.midtop

        # Сохраняет позицию снаряда в вещественном формате.
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану."""
        # Обновляет y, не rect.
        self.y -= self.settings.bullet_speed

        # Перемещает корабль.
        self.rect.y = self.y

    def draw_bullet(self):
        """Рисует снаряды на экране."""
        pygame.draw.rect(self.screen, self.color, self.rect)

