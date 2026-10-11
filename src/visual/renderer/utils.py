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

    def tint(self, img: Any, color: Any) -> Any:
        """Return a copy of img multiplied by color (alpha preserved).

        The color is lifted a bit towards white so dark colors
        (black, navy...) don't turn the sprite into an invisible blob.
        """
        lifted = color.lerp(pygame.Color(255, 255, 255), 0.25)
        tinted: Any = img.copy()
        tinted.fill(
            (lifted.r, lifted.g, lifted.b, 255),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        return tinted
