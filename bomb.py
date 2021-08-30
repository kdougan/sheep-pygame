import pygame
from assets import asset_sheet
from base import Base
from config import gravity
from display import display


class BombManager:
    def __init__(self, game):
        surf = asset_sheet.subsurface(pygame.Rect(16, 0, 16, 16))
        self.bomb_surf = surf.subsurface(surf.get_bounding_rect())
        self.bombs = []
        self.held = None
        self.game = game

        self.impacts = []

    def update(self, dt):
        [bomb.update(dt) for bomb in self.bombs]
        impacts = []
        if self.held:
            bomb = self.held
            ground_height = self.game.ground_manager.get_ground_height(
                int(bomb.center.x))
            mouse_pos = self.game.display_mouse_position
            bomb.pos.x = max(0,
                             min(mouse_pos.x-(bomb.size.x*0.5),
                                 display.get_width()-bomb.size.x))
            bomb.pos.y = max(0,
                             min(mouse_pos.y-(bomb.size.y*0.5),
                                 ground_height-bomb.size.y))
        else:
            for bomb in self.bombs:
                ground_height = self.game.ground_manager.get_ground_height(
                    int(bomb.center.x))
                if bomb.bottom >= ground_height:
                    bomb.pos.y = bomb.size.y + ground_height
                    bomb.alive = False
                    impacts.append(bomb)
                    self.game.shake_display()
        self.game.sheep_manager.evaluate_impacts(impacts)
        self.bombs[:] = [bomb for bomb in self.bombs if bomb.alive]

    def render(self, surf):
        [bomb.render(surf) for bomb in self.bombs]

    def create_held_bomb(self, pos):
        if self.held:
            return
        bomb = self.create_bomb(pos, (0, 0), True)
        self.held = bomb

    def create_bomb(self, pos, vel, held=False):
        bomb = Bomb(self.bomb_surf, pos, vel, held)
        self.bombs.append(bomb)
        return bomb

    def drop(self):
        if self.held:
            self.held.held = False
            self.held = None


class Bomb(Base):
    def __init__(self, surf, pos, vel, held=False):
        self.surf = surf
        self.size = pygame.Vector2(self.surf.get_size())
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.alive = True
        self.held = held

    def update(self, dt):
        if self.held:
            return
        self.vel += pygame.Vector2(0, gravity*dt)
        self.pos += pygame.Vector2([i*dt for i in self.vel])

    def render(self, surf):
        surf.blit(self.surf, self.pos)
