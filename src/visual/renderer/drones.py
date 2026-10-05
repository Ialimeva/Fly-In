import pygame
from typing import Any


class DronesRenderer:
    def __init__(self, actions_per_turn: dict[int, Any], coordinates: dict[str, Any], buffer: Any) -> None:
        raw_img: Any = pygame.image.load("src/visual/assets/drone.png")
        tile_size: int = 32

        self.frames: dict[int, Any] = {}
        for i in range(6):
            img: Any = pygame.Surface((tile_size, tile_size)).convert_alpha()
            start_w, start_h = (i * tile_size, i * tile_size)
            end_w, end_h = (start_w + tile_size, start_h + tile_size)
            img.blit(raw_img, (0, 0), (start_w, start_h, end_w, end_h))

            self.frames[i] = img

        self.actions_per_turn: dict[int, Any] = actions_per_turn
        self.coordinates: dict[str, Any] = coordinates
        self.buffer: Any = buffer
        self.frame_index: int = 0
    
    def draw_drones(self) -> None:
        for turn, actions in self.actions_per_turn.items():
            if turn == 0:
                    for action in actions:
                        target: str = action["target"]
                        if "-" in target:
                            continue
                        self.buffer.blit(self.frames[self.frame_index], self.coordinates[target])