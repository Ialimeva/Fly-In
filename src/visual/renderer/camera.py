import pygame
from typing import Any


class Camera:
    def __init__(self, window: Any, graph_buffer: Any) -> None:
        self.speed: int = 20
        self.window: Any = window
        self.graph_buffer: Any = graph_buffer
        self.window_w, self.window_h = self.window.get_rect().size
        self.buffer_w, self.buffer_h = self.graph_buffer.get_rect().size
        # Screen position of the graph buffer's (0, 0) pixel.
        self.origin: tuple[int, int] = (0, 0)

    def world_to_screen(self, x: float, y: float) -> tuple[float, float]:
        return (x + self.origin[0], y + self.origin[1])

    def present(self, cam_x: int, cam_y: int) -> tuple[int, int]:
        offset_x = max(0, (self.window_w - self.buffer_w) // 2)
        offset_y = max(0, (self.window_h - self.buffer_h) // 2)

        max_cam_x = max(0, self.buffer_w - self.window_w)
        max_cam_y = max(0, self.buffer_h - self.window_h)
        cam_x = max(0, min(cam_x, max_cam_x))
        cam_y = max(0, min(cam_y, max_cam_y))

        visible_w = min(self.buffer_w, self.window_w)
        visible_h = min(self.buffer_h, self.window_h)

        self.origin = (offset_x - cam_x, offset_y - cam_y)
        self.window.blit(
            self.graph_buffer,
            (offset_x, offset_y),
            area=pygame.Rect(cam_x, cam_y, visible_w, visible_h)
        )

        # Return the clamped values so the caller never drifts past the edge.
        return cam_x, cam_y
