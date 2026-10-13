"""
Playback controls drawn above the animation.

This module draws and handles everything the user can use to
control the playback: buttons, turn information, the moves of the
paused turn and the progress bar.

Extracted class:
    Hud: Draw the controls and handle clicks on them.
"""
import pygame
from typing import Any


class Hud:
    """
    Draw the playback controls and handle clicks on them.

    Attributes:
        window: Pygame window.
        drones: Drones renderer, source of the playback state.
        w: Window width.
        h: Window height.
        font_big: Font of the turn number.
        font: Font of the status.
        font_small: Font of the help and the moves.
        buttons: Rectangle of each button, by name.
        info_rect: Rectangle of the turn information panel.
        bar: Rectangle of the progress bar at the bottom of the window,
        created here and drawn each frame by draw_bar.
        _bg: Cache of the translucent panel backgrounds.
    """
    def __init__(self, window: Any, drones: Any) -> None:
        self.window: Any = window
        self.drones: Any = drones
        self.w, self.h = window.get_size()

        self.font_big: Any = pygame.font.Font(None, 36)
        self.font: Any = pygame.font.Font(None, 24)
        self.font_small: Any = pygame.font.Font(None, 20)

        names = ("prev", "play", "next", "restart", "slower", "faster")
        self.buttons: dict[str, Any] = {
            name: pygame.Rect(16 + i * (44 + 9), 16, 44, 44)
            for i, name in enumerate(names)
        }
        strip_w: int = len(names) * 44 + (len(names) - 1) * 9
        self.info_rect = pygame.Rect(16, 16 + 44 + 9, strip_w, 108)
        self.bar = pygame.Rect(16, self.h - 16 - 18, self.w - 2 * 16, 18)
        self._bg: dict[tuple[int, int, int], Any] = {}

    def handle_click(self, pos: tuple[int, int]) -> bool:
        """Run the clicked button or seek a turn, True if on the hud."""
        d: Any = self.drones
        actions: dict[str, Any] = {
            "prev": lambda: d.step(-1),
            "play": d.toggle_pause,
            "next": lambda: d.step(1),
            "restart": d.restart,
            "slower": lambda: d.change_speed(-1),
            "faster": lambda: d.change_speed(1),
        }
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                actions[name]()
                return True

        return self.info_rect.collidepoint(pos)

    def panel(self, rect: Any, alpha: int = 165) -> None:
        """Draw a translucent rounded background, cached."""
        key = (rect.w, rect.h, alpha)
        if key not in self._bg:
            surf = pygame.Surface(rect.size, pygame.SRCALPHA)
            pygame.draw.rect(
                surf, (12, 14, 24, alpha), surf.get_rect(), border_radius=12
            )
            self._bg[key] = surf
        self.window.blit(self._bg[key], rect.topleft)

    def text(
        self,
        font: Any,
        msg: str,
        color: Any,
        pos: tuple[int, int]
    ) -> None:
        """Draw a text with a shadow."""
        self.window.blit(
            font.render(msg, True, (0, 0, 0)),
            (pos[0] + 1, pos[1] + 1)
        )
        self.window.blit(font.render(msg, True, color), pos)

    def icon(self, name: str, rect: Any) -> None:
        """Draw the icon of a button."""
        w: Any = self.window
        cx, cy = rect.center
        d: Any = self.drones
        if name == "play":
            if d.paused or d.finished:
                pygame.draw.polygon(
                    w, (255, 255, 255),
                    [(cx - 7, cy - 11), (cx - 7, cy + 11), (cx + 11, cy)]
                )
            else:
                pygame.draw.rect(w, (255, 255, 255), (cx - 9, cy - 11, 6, 22))
                pygame.draw.rect(w, (255, 255, 255), (cx + 3, cy - 11, 6, 22))
        elif name == "prev":
            pygame.draw.rect(w, (255, 255, 255), (cx - 11, cy - 10, 3, 20))
            pygame.draw.polygon(
                w, (255, 255, 255), [
                    (cx + 10, cy - 10),
                    (cx + 10, cy + 10),
                    (cx - 6, cy)
                ]
            )
        elif name == "next":
            pygame.draw.rect(w, (255, 255, 255), (cx + 8, cy - 10, 3, 20))
            pygame.draw.polygon(
                w, (255, 255, 255), [
                    (cx - 10, cy - 10),
                    (cx - 10, cy + 10),
                    (cx + 6, cy)
                ]
            )
        elif name == "restart":
            pygame.draw.arc(
                w, (255, 255, 255), pygame.Rect(
                    cx - 10,
                    cy - 10,
                    20, 20
                ), 0.9, 6.0, 3
            )
            pygame.draw.polygon(
                w, (255, 255, 255), [
                    (cx + 3, cy - 14),
                    (cx + 3, cy - 4),
                    (cx + 12, cy - 9)
                ]
            )
        elif name == "slower":
            pygame.draw.rect(w, (255, 255, 255), (cx - 9, cy - 2, 18, 4))
        elif name == "faster":
            pygame.draw.rect(w, (255, 255, 255), (cx - 9, cy - 2, 18, 4))
            pygame.draw.rect(w, (255, 255, 255), (cx - 2, cy - 9, 4, 18))

    def draw(self) -> None:
        """Draw buttons, information, progress bar and paused moves."""
        d: Any = self.drones
        mouse: tuple[int, int] = pygame.mouse.get_pos()

        for name, rect in self.buttons.items():
            self.panel(rect, 200)
            if rect.collidepoint(mouse):
                pygame.draw.rect(
                    self.window,
                    (255, 255, 255),
                    rect,
                    2,
                    border_radius=12
                )
            self.icon(name, rect)

        self.draw_info()
        if d.paused:
            self.draw_moves()

    def draw_info(self) -> None:
        """Draw the turn, status, speed and keyboard help."""
        d: Any = self.drones
        r: Any = self.info_rect
        self.panel(r)

        self.text(
            self.font_big,
            f"Turn {d.display_turn} / {d.max_turn}",
            (255, 255, 255),
            (r.x + 10, r.y + 8)
        )

        if d.finished:
            status, color = "FINISHED (press R)", (110, 230, 140)
        elif d.paused:
            status, color = "PAUSED", (255, 210, 60)
        else:
            status, color = "PLAYING", (120, 190, 255)
        extra: str = ""
        k: int = int(d.time)
        if not d.finished and d.time - k > 1e-6:
            extra = f"  {k}->{k + 1}  {int((d.time - k) * 100)}%"
        self.text(
            self.font,
            f"{status}  x{d.speed:g}{extra}",
            color,
            (r.x + 10, r.y + 40)
        )

        self.text(
            self.font_small,
            "SPACE pause | , . step | R restart",
            (170, 175, 190),
            (r.x + 10, r.y + 66)
        )
        self.text(
            self.font_small,
            "+/- speed | arrows or drag: pan",
            (170, 175, 190),
            (r.x + 10, r.y + 84)
        )

    def draw_bar(self) -> None:
        """Draw the progress bar, turn marks and handle from time."""
        d: Any = self.drones
        bar: Any = self.bar
        self.panel(bar.inflate(8, 8), 170)

        frac: float = d.time / d.max_turn if d.max_turn else 1.0
        fill = pygame.Rect(bar.x, bar.y, int(bar.w * frac), bar.h)
        pygame.draw.rect(self.window, (70, 150, 230), fill, border_radius=8)

        if 0 < d.max_turn <= 100:
            for t in range(d.max_turn + 1):
                x: int = bar.x + int(bar.w * t / d.max_turn)
                pygame.draw.line(
                    self.window,
                    (255, 255, 255),
                    (x, bar.y + 12),
                    (x, bar.bottom - 1),
                    1
                )

        pygame.draw.circle(
            self.window,
            (255, 255, 255),
            (bar.x + int(bar.w * frac), bar.centery),
            9
        )

    def draw_moves(self) -> None:
        """Draw the list of moves of the paused turn."""
        d: Any = self.drones
        turn: int = d.display_turn
        moves = d.moves(turn)
        lines: list[str] = []
        if turn == 0:
            lines.append(f"{len(d.tracks)} drones at start")
        else:
            lines = [f"D{dr}: {a} -> {b}" for dr, a, b in moves[:14]]
            if len(moves) > 14:
                lines.append(f"... +{len(moves) - 14} more")
            waiting: int = len(d.tracks) - len(moves)
            lines.append(f"({waiting} waiting)")

        rect = pygame.Rect(self.w - 316, 16, 300, 38 + 20 * len(lines))
        self.panel(rect)
        self.text(
            self.font,
            f"Turn {turn} moves",
            (255, 210, 60),
            (rect.x + 10, rect.y + 8)
        )
        for i, line in enumerate(lines):
            self.text(
                self.font_small,
                line,
                (255, 255, 255),
                (rect.x + 10, rect.y + 34 + 20 * i)
            )
