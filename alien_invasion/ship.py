import pygame

class Ship:
    """Класс для хранения настроек космического корабля игры Alien Invasion."""

    def __init__(self, ai):
        """Инициализирует корабль и задаёт его начальную позицию."""
        self.screen = ai.screen
        self.settings = ai.settings
        self.screen_rect = ai.screen.get_rect()

        # Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Выравнивает низ середины изображения корабля по низу середины
        # изображения экрана.
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты корабля.
        self.x = float(self.rect.x)

        # Флаг отвечающий за движение корабля.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляет атрибут x, не rect."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Обновление атрибута rect на основании self.x:
        self.rect.x = self.x

    def start_pozition(self):
        """Перерисовывает корабль в стартовой позиции."""
        # Выравнивает низ середины изображения корабля по низу середины
        # изображения экрана.
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты корабля.
        self.x = float(self.rect.x)


    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)
