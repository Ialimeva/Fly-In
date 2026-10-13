"""
Simulate camera movement on window.

This module simulate camera mouvement on the
window and graph.

Exported class:
    Camera: Simulate camera mouvement on window.
"""
import pygame
from typing import Any


class Camera:
    """
    Simulate camera movement on window.

    Attributes:
        speed: Camera mouvement speed.
        window: Pygame window.
        graph_buffer: Rendered graph buffer.
        window_w: Window width.
        window_h: Window height.
        buffer_w: Graph buffer width.
        buffer_h: Graph buffer height.
        origin: Render destination on window.
    """
    def __init__(self, window: Any, graph_buffer: Any) -> None:
        self.speed: int = 20
        self.window: Any = window
        self.graph_buffer: Any = graph_buffer
        self.window_w, self.window_h = self.window.get_rect().size
        self.buffer_w, self.buffer_h = self.graph_buffer.get_rect().size

        self.origin: tuple[int, int] = (0, 0)

    def world_to_screen(self, x: float, y: float) -> tuple[float, float]:
        """Return render destination on window."""
        return (x + self.origin[0], y + self.origin[1])

    def present(self, cam_x: int, cam_y: int) -> tuple[int, int]:
        """Render graph buffer on window."""
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

        return cam_x, cam_y 
