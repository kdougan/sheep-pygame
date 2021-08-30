from base import Base
import pygame
from assets import asset_sheet
from display import display
from config import ground_height


class GroundManager:
    def __init__(self, game):
        self.ground_list = [Ground((i, ground_height))
                            for i in range(display.get_width())]
        self.game = game

    def update(self, _):
        for i, current in enumerate(self.ground_list):
            has_prev = i >= 1
            has_next = i+1 < len(self.ground_list)
            previous_g = self.ground_list[i-1] if has_prev else current
            next_g = self.ground_list[i+1] if has_next else current
            if (has_prev and
                current.height > previous_g.height+1 and
                    previous_g.height <= next_g.height):
                previous_g.increment()
                current.decrement()
            if (has_next and
                current.height > next_g.height+1 and
                    next_g.height <= previous_g.height):
                next_g.increment()
                current.decrement()

        lowest = min(self.ground_list, key=lambda x: x.pos.y)
        for ground in self.ground_list:
            ground.pos.y -= (lowest.pos.y - 1)

        self.game.score_manager.add_peak(
            max(self.ground_list, key=lambda x: x.height).height)

    def render(self, surf):
        [ground.render(surf) for ground in self.ground_list]

    def get_ground_height(self, index):
        if index < 0:
            index = 0
        elif index >= len(self.ground_list):
            index = len(self.ground_list)-1
        return display.get_height()-self.ground_list[index].pos.y

    def increment(self, index):
        self.ground_list[index].increment()


class Ground(Base):
    def __init__(self, pos):
        self.surf = asset_sheet.subsurface(pygame.Rect(32, 0, 1, 16))
        self.size = pygame.Vector2(self.surf.get_size())
        self.pos = pygame.Vector2(pos)
        self.height = 1

    def render(self, surf):
        display_height = display.get_height()
        surf.blit(
            self.surf,
            pygame.Vector2(
                self.pos.x,
                display_height-self.pos.y
            )
        )
        y = self.pos.y-self.size.y
        if y > 0:
            pygame.draw.line(
                display,
                (0, 0, 0),
                (self.pos.x, display_height-y),
                (self.pos.x, display_height)
            )

    def increment(self):
        self.height += 1
        self.pos.y += 1

    def decrement(self):
        self.height -= 1
        self.pos.y -= 1
