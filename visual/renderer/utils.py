"""
Render utilities.

This module gives all render utilities.

Exported class:
    Utils: Render utilities.
"""
import pygame
from typing import Any


class Utils:
    """Render utilities."""
    def scale_img(self, img: Any, coords: tuple[int, int]) -> Any:
        """Scale given image surface"""
        return pygame.transform.scale(img, coords)

    def crop_img(self, img: Any) -> Any:
        """Crop image to only visible pixels"""
        bound = img.get_bounding_rect()

        return img.subsurface(bound).copy()

    def parse_color(self, name: Any) -> Any | None:
        """Parse pygame color instance."""
        try:
            return pygame.Color(name.lower())
        except ValueError:
            return None
