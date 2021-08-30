import random

import pygame
from assets import asset_sheet
from base import Base
from config import gravity
from display import display


class GibManager:
    def __init__(self, game):
        self.gibs = []
        self.gib_surfs = [
            asset_sheet.subsurface(pygame.Rect((i*16)+48, 0, 16, 16))
            for i in range(5)
        ]
        self.game = game

    @property
    def gib_count(self):
        return len(self.gibs)

    def update(self, dt):
        [gib.update(dt) for gib in self.gibs]
        for gib in self.gibs:
            ground_height = self.game.ground_manager.get_ground_height(
                int(gib.center.x))
            if gib.pos.x < 0 or gib.pos.x > display.get_width()-1:
                gib.pos.x = max(0, min(gib.pos.x, display.get_width()-1))
                gib.vel.x = 0
                if random.random() > .1:
                    gib.alive = False

            if gib.alive and gib.pos.y >= ground_height:
                if random.random() > .5:
                    self.game.ground_manager.increment(int(gib.pos.x))
                gib.alive = False
        self.gibs[:] = [gib for gib in self.gibs if gib.alive]

    def render(self, surf):
        [gib.render(surf) for gib in self.gibs]

    def spawn(self, pos, count):
        _min = max(count-10, 0)
        _max = count+10
        for _ in range(random.randint(_min, _max)):
            surf = random.choice(self.gib_surfs)
            self.gibs.append(
                Gib(
                    surf=pygame.transform.rotate(surf.subsurface(
                        surf.get_bounding_rect()), random.randint(0, 360)),
                    pos=pos,
                    vel=[random.uniform(-200, 200),
                         random.uniform(-400, -100)],
                    lifetime=random.randint(2, 8)
                )
            )


class Gib(Base):
    def __init__(self, surf, pos, vel, lifetime):
        self.surf = surf
        self.size = pygame.Vector2(self.surf.get_size())
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.lifetime = lifetime
        self.age = 0
        self.alive = True

    def update(self, dt):
        self.vel += pygame.Vector2(0, gravity*dt)
        self.pos += pygame.Vector2([i*dt for i in self.vel])
        self.age += dt
        self.alive = self.age <= self.lifetime

    def render(self, surf):
        surf.blit(self.surf, self.pos)
