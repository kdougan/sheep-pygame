# coding: utf-8

import random
from score import ScoreManager
import sys
import time

import pygame
from display import display
from display import window
from bomb import BombManager
from gib import GibManager
from ground import GroundManager
from sheep import SheepManager

clock = pygame.time.Clock()

pygame.mouse.set_visible(False)


class Game:
    def __init__(self):
        self.shake_amount = 16
        self.shake_duration = .1
        self.shake_recovery = .95
        self.shake_timer = 0

        self.sheep_timer = 0
        self.sheep_timer_max = .5
        self.sheep_timer_min = .1
        self.max_sheep_count = 500

        self.held = None

        self.score_manager = ScoreManager(self)
        self.ground_manager = GroundManager(self)
        self.gib_manager = GibManager(self)
        self.bomb_manager = BombManager(self)
        self.sheep_manager = SheepManager(self)

        self.t = 0
        self.dt = 1/60
        self.current_time = time.perf_counter()

        display_size = display.get_size()
        pygame.mouse.set_pos(display_size[0]*0.5, display_size[1]*0.5)

        self.shake = pygame.Vector2(0, 0)

    @property
    def mouse_position(self):
        return pygame.Vector2(pygame.mouse.get_pos())

    @property
    def display_mouse_position(self):
        return self.mouse_position * 0.5

    def run(self):
        while 1:
            new_time = time.perf_counter()
            frame_time = new_time-self.current_time
            self.current_time = new_time

            for event in pygame.event.get():
                if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and
                     event.key == pygame.K_ESCAPE)):
                    pygame.quit()
                    sys.exit()
                elif (event.type == pygame.KEYDOWN and
                        event.key == pygame.K_TAB):
                    self.score_manager.print_stats()

            self.handle_mouse()
            self.handle_keyboard()

            while frame_time > 0:
                delta_time = min([frame_time, self.dt])
                self.update(delta_time)
                frame_time -= self.dt
                self.t += delta_time

            self.render()
            clock.tick(60)

    def handle_mouse(self):
        m_pressed = pygame.mouse.get_pressed()
        if m_pressed[0]:
            self.bomb_manager.create_held_bomb(self.display_mouse_position)
        else:
            self.bomb_manager.drop()

    def handle_keyboard(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            self.sheep_manager.create_sheep(
                (random.uniform(16, display.get_width() - 32),
                 random.randint(0, 100)),
                (random.uniform(20, 60) * random.choice([1, -1]), 0),
            )

    def shake_display(self):
        self.shake_timer = self.shake_duration

    def update(self, dt):
        self.shake_timer = max([self.shake_timer-dt, 0])
        if self.shake_timer > 0:
            self.shake_timer -= dt
            self.shake = pygame.Vector2(
                [random.uniform(-self.shake_amount, self.shake_amount) for _ in range(2)])
        if self.shake.x != 0:
            self.shake.x *= self.shake_recovery
        if self.shake.y != 0:
            self.shake.y *= self.shake_recovery
        if abs(self.shake.x) < .01:
            self.shake.x = 0
        if abs(self.shake.y) < .01:
            self.shake.y = 0

        self.sheep_timer -= dt
        if self.sheep_timer <= 0 and self.sheep_manager.sheep_count < self.max_sheep_count:
            self.sheep_timer = random.uniform(
                self.sheep_timer_min, self.sheep_timer_max)
            self.sheep_manager.create_sheep(
                (random.uniform(16, display.get_width() - 32),
                 random.randint(0, 100)),
                (random.uniform(20, 60) * random.choice([1, -1]), 0),
            )

        self.sheep_manager.update(dt)
        self.bomb_manager.update(dt)
        self.gib_manager.update(dt)
        self.ground_manager.update(dt)

    def render(self):
        window.fill((0, 0, 0))
        display.fill((60, 50, 60))

        self.gib_manager.render(display)
        self.sheep_manager.render(display)
        self.bomb_manager.render(display)
        self.ground_manager.render(display)
        self.score_manager.render(display)

        pygame.draw.circle(display, (0, 0, 0),
                           self.display_mouse_position, 5, 2)
        pygame.draw.circle(display, (0, 200, 0),
                           self.display_mouse_position, 4, 1)

        scaled_display = pygame.transform.scale(display, window.get_size())
        window.blit(scaled_display, self.shake)
        pygame.display.update()


Game().run()
