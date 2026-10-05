import pygame
from typing import Any
from .utils import Utils


class BackgroundRenderer:
    def __init__(self, utils: Utils, window: Any) -> None:
        self.utils: Utils = utils
        self.window: Any = window
        self.window_w, self.window_h = self.window.get_rect().size

        self.backs: list[Any] = []
        for i in range(1, 155):
            raw: Any = pygame.image.load(
                f"src/visual/assets/background/{i}.jpg"
            ).convert()
            raw = self.utils.scale_img(raw, (self.window_w, self.window_h))
            self.backs.append(raw)

        self.frame_index: int = 0
        self.frame_duration: int = 40
        self.last_switch: int = pygame.time.get_ticks()

    def draw(self) -> None:
        frame: Any = self.backs[self.frame_index]

        self.window.blit(frame, (0, 0))

    def animate(self) -> None:
        now: int = pygame.time.get_ticks()
        if now - self.last_switch > self.frame_duration:
            self.frame_index = (self.frame_index + 1) % len(self.backs)
            self.last_switch = now

        self.draw()
