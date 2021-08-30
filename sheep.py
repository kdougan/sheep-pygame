import random

import pygame
from assets import asset_sheet
from base import Base
from config import gravity
from display import display


class SheepManager:
    def __init__(self, game):
        surf = asset_sheet.subsurface(pygame.Rect(0, 0, 16, 16))
        self.sheep_surf = surf.subsurface(surf.get_bounding_rect())
        self.sheep = []
        self.game = game

    @property
    def sheep_count(self):
        return len(self.sheep)

    def create_sheep(self, pos, vel):
        self.sheep.append(Sheep(self.sheep_surf, pos, vel))

    def update(self, dt):
        [sheep.update(dt) for sheep in self.sheep]
        for sheep in self.sheep:
            ground_pos = self.game.ground_manager.get_ground_height(
                int(sheep.center.x))
            display_width = display.get_width()

            if sheep.pos.y + sheep.size.y >= ground_pos:
                sheep.pos.y = ground_pos - sheep.size.y
                sheep.vel.y = random.uniform(-100, -200)

            if sheep.pos.x < 0 or sheep.pos.x + sheep.size.x > display_width:
                sheep.vel.x *= -1
                sheep.pos.x = max(
                    0, min(sheep.pos.x, display_width-sheep.size.x))
        self.sheep[:] = [sheep for sheep in self.sheep if sheep.alive]

    def evaluate_impacts(self, impacts):
        removed = 0
        for bomb in impacts:
            for sheep in self.sheep:
                dist = sheep.center.distance_to(bomb.center)
                if dist < 64:
                    sheep.alive = False
                    removed += 1
                    self.game.gib_manager.spawn(sheep.center,
                                                random.randint(10, 30))
                elif sheep.alive and dist < 512:
                    if (random.random() > (dist - 64) / (512 - 64) and
                        ((sheep.center.x > bomb.center.x and sheep.vel.x < 0) or
                            (sheep.center.x < bomb.center.x and sheep.vel.x > 0))):
                        sheep.vel.x *= -2
        self.game.score_manager.add_score(removed)

    def render(self, surf):
        [sheep.render(surf) for sheep in self.sheep]


class Sheep(Base):
    def __init__(self, surf, pos, vel):
        self.surf = surf
        self.size = pygame.Vector2(self.surf.get_size())
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.direction = True
        self.alive = True

    def update(self, dt):
        self.vel += pygame.Vector2(0, gravity*dt)
        self.vel.x = max(min(self.vel.x, 200), -200)
        self.pos += pygame.Vector2([i*dt for i in self.vel])
        if self.direction != (self.vel.x < 0):
            self.direction = self.vel.x < 0
            self.surf = pygame.transform.flip(self.surf, True, False)

    def render(self, surf):
        surf.blit(self.surf, self.pos)
