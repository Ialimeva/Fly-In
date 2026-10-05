import pygame
from typing import Any
from .utils import Utils


class DronesRenderer:
    def __init__(
        self,
        actions_per_turn: dict[int, Any],
        coordinates: dict[str, Any],
        buffer: Any, utils: Utils
    ) -> None:
        raw_img: Any = pygame.image.load(
            "src/visual/assets/drone.png"
        ).convert_alpha()
        tile_size: int = 32

        img: Any = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        img.blit(raw_img, (0, 0), (0, 0, tile_size, tile_size))

        self.drone_img = utils.scale_img(img, (64, 64))
 
        self.actions_per_turn: dict[int, Any] = actions_per_turn
        self.coordinates: dict[str, Any] = coordinates
        self.buffer: Any = buffer

    def draw_drone(self, coordinates: Any) -> None:
        self.buffer.blit(
            self.drone_img,
            coordinates
        )

    def draw_turn(
        self
    ) -> None:
        for turn, actions in self.actions_per_turn.items():
            if turn == 0:
                    for action in actions:
                        target: str = action["target"]
                        if "-" in target:
                            continue
                        self.draw_drone(
                            self.coordinates[target]
                        )

