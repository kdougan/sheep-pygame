import pygame
from display import display
from assets import number_sheet
from config import display_padding


class ScoreManager:
    def __init__(self, game):
        surfs = [number_sheet.subsurface(pygame.Rect(i*16, 0, 16, 16))
                 for i in range(10)]
        self.number_surfs = [surf.subsurface(surf.get_bounding_rect())
                             for surf in surfs]
        self.game = game
        self.score = 0
        self.max_combo = 0
        self.highest_peak = 0

    def add_score(self, score):
        self.score += score
        if score > self.max_combo:
            self.max_combo = score

    def add_peak(self, peak):
        if peak > self.highest_peak:
            self.highest_peak = peak

    def print_stats(self):
        print('Stats:')
        print(f' - score: {self.score}')
        print(f' - max combo: {self.max_combo}')
        print(f' - highest peak: {self.highest_peak}')

    def create_score_surf(self):
        score_surfs = [self.number_surfs[int(i)].copy()
                       for i in str(self.score)]
        total_width = sum(surf.get_width()
                          for surf in score_surfs) + ((len(score_surfs) - 1) * 2)
        score_surf = pygame.Surface(
            (total_width, score_surfs[0].get_height()), pygame.SRCALPHA)
        offset = 0
        for surf in score_surfs:
            score_surf.blit(surf, (offset, 0))
            offset += surf.get_width() + 2
        return score_surf

    def update(self, _):
        pass

    def render(self, surf):
        surface = pygame.Surface(display.get_size(), pygame.SRCALPHA)

        score_surf = self.create_score_surf()
        surface.blit(score_surf,
                     (display.get_width() - score_surf.get_width() - display_padding, display_padding))

        surf.blit(surface, (0, 0))
