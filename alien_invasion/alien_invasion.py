import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # Создаёт экземпляр игровой статистики.
        self.game_stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.button = Button(self)
        self._create_fleet()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            if self.game_stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien()
            self._update_screen()

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_events_down(event)
            elif event.type == pygame.KEYUP:
                self._check_events_up(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_mouse_button(mouse_pos)

    def _check_mouse_button(self, mouse_pos):
        """Отслеживание нажатий на мышь."""
        button_click = self.button.rect.collidepoint(mouse_pos)
        if button_click and not self.game_stats.game_active:
            # Сброс игровой статистики.
            self.settings._increase_speed()
            self.game_stats.reset_stats()
            self.game_stats.game_active = True

            self._start_game()
            # Курсор мыши исчезает.
            pygame.mouse.set_visible(False)

    def _start_game(self):
        """Удаляет остатки пришельцев, создаёт новый флот и выравнивает корабль
        по центру."""
        # Удаление остатков снарядов и пришельцев.
        self.aliens.empty()
        self.bullets.empty()
        # Создание нового флота и выравнивание корабля по центру.
        self._create_fleet()
        self.ship.start_pozition()

    def _check_events_down(self, event):
        """Отслеживание нажатий на клавиши."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()
        elif event.key == pygame.K_p:
            self.game_stats.game_active = True

    def _check_events_up(self,event):
        """Отслеживание отпусканий на клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullets(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Управляет снарядами на экране."""
        # Обновление позиций снарядов.
        self.bullets.update()

        # Уничтожение старых снарядов.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Проверяет коллизии, уничтожает оставшиеся снаряды и создаёт новый
        флот."""
        # Проверка попаданий в пришельцев.
        # При обнаружении попаданий удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)
        if not self.aliens:
            # Уничтожает оставшиеся снаряды после уничтожения флота и создаёт
            # новый флот, увеличивает скорость игры.
            self.bullets.empty()
            self._create_fleet()
            self.settings.new_speed()

    def _create_fleet(self):
        """Создаёт флот пришельцев."""
        # Считает сколько пришельцев уместится по горизонтали экрана.
        alien = Alien(self)
        available_aliens = self.settings.screen_width - 2*alien.rect.width
        numbers_alien = available_aliens//(2*alien.rect.width)

        # Вычисления количества рядов пришельцев.
        available_aliens_y = (self.settings.screen_height - 4*alien.rect.height
                                - self.ship.rect.height)
        numbers_row = available_aliens_y//(2*alien.rect.height)

        # Цикл для создания флота.
        for row_number in range(numbers_row):
            for alien_number in range(numbers_alien):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создаёт одного пришельца."""
        alien = Alien(self)
        alien.x = alien.rect.width + 2*alien.rect.width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Проверяет, что флот достиг края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает флот ниже и меняет направление движения."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_alien(self):
        """Проверяет, что флот у края экрана и обновляет позицию пришельца."""
        self._check_fleet_edges()
        self.aliens.update()
        # Проверяет коллизии между кораблём и пришельцами.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Проверяет, добрался ли пришелец до низа экрана.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Если пришелец добрался до нижнего края экрана, то игра
        перезапускается."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """При столкновении пришельца с кораблём вносит изменения в игру."""
        if self.game_stats.ship_left > 0:
            # Уменьшает количество кораблей.
            self.game_stats.ship_left -= 1

            self._start_game()
            # Даёт игроку паузу в 0.5 секунды, чтобы приготовиться.
            sleep(0.5)
        else:
            self.game_stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Перерисовывает экран и отображает последний прорисованный экран."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.game_stats.game_active:
            self.button.blitme()
        pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()


