import pygame
from typing import Any


class Utils:
    def scale_img(self, img: Any, coords: tuple[int, int]) -> Any:
        return pygame.transform.scale(img, coords)

    def crop_img(self, img: Any) -> Any:
        bound = img.get_bounding_rect()

        return img.subsurface(bound).copy()

    def parse_color(self, name: str | None) -> Any | None:
        try:
            return pygame.Color(name.lower())
        except ValueError:
            return None

