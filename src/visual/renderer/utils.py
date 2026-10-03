import pygame
from typing import Any


class Utils:
    def scale_img(self, img: Any, coords: tuple[int, int]) -> Any:
        return pygame.transform.scale(img, coords)

    def crop_img(self, img: Any) -> Any:
        bound = img.get_bounding_rect()

        return img.subsurface(bound).copy()