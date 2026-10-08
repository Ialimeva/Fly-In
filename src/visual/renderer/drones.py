import math
import pygame
from typing import Any
from .utils import Utils

NODE: int = 64
SPEEDS: tuple[float, ...] = (0.25, 0.5, 1.0, 2.0, 4.0)


def ease(f: float) -> float:
    return f * f * (3 - 2 * f)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def spread(i: int, n: int) -> tuple[float, float]:
    """Offset of the i-th drone out of n sharing the same zone."""
    if n <= 1:
        return (0.0, 0.0)
    if n <= 7:
        angle: float = 2 * math.pi * i / n - math.pi / 2
        return (20 * math.cos(angle), 20 * math.sin(angle))
    if i == 0:
        return (0.0, 0.0)
    ring, left = 1, i - 1
    while left >= 6 * ring:
        left -= 6 * ring
        ring += 1
    angle = 2 * math.pi * left / (6 * ring)
    return (22 * ring * math.cos(angle), 22 * ring * math.sin(angle))


def size_for(n: int) -> int:
    if n <= 1:
        return 64
    return 48 if n <= 7 else 34


class DronesRenderer:
    def __init__(
        self,
        actions_per_turn: dict[int, Any],
        coordinates: dict[str, Any],
        window: Any,
        utils: Utils
    ) -> None:
        raw_img: Any = pygame.image.load(
            "src/visual/assets/drone.png"
        ).convert_alpha()
        tile_size: int = 32

        self.base_img: Any = pygame.Surface(
            (tile_size, tile_size), pygame.SRCALPHA
        )
        self.base_img.blit(raw_img, (0, 0), (0, 0, tile_size, tile_size))

        self.actions_per_turn: dict[int, Any] = actions_per_turn
        self.coordinates: dict[str, Any] = coordinates
        self.window: Any = window
        self.utils: Utils = utils

        self.font: Any = pygame.font.Font(None, 20)
        self._sprites: dict[int, Any] = {}
        self._labels: dict[int, Any] = {}

        # Playback state
        self.tracks: dict[int, list[str]] = {}
        self.slots: list[dict[int, tuple[int, int]]] = []
        self.max_turn: int = 0
        self.time: float = 0.0      # in turns; 3.5 = halfway through 3 -> 4
        self.anim: float = 0.0      # hover clock, frozen while paused
        self.paused: bool = False
        self.speed_index: int = 2

    # ---------- timeline ----------

    def build_timeline(self) -> None:
        """Build one position-per-turn track for every drone.

        Called from Visual.start(): actions_per_turn is only filled once the
        simulation has run, i.e. after this renderer was constructed.
        The track is built from each action's *target* only, so it doesn't
        depend on the "source" field.
        """
        self.max_turn = max(self.actions_per_turn, default=0)

        raw: dict[int, dict[int, str]] = {}
        for turn, actions in self.actions_per_turn.items():
            for action in actions:
                raw.setdefault(action["D"], {})[turn] = action["target"]

        self.tracks = {}
        for drone in sorted(raw):
            by_turn: dict[int, str] = raw[drone]
            last: str = by_turn[min(by_turn)]
            track: list[str] = []
            for turn in range(self.max_turn + 1):
                last = by_turn.get(turn, last)
                track.append(last)
            self.tracks[drone] = track

        # How many drones share a zone/link each turn (to spread them out).
        self.slots = []
        for turn in range(self.max_turn + 1):
            groups: dict[str, list[int]] = {}
            for drone, track in self.tracks.items():
                groups.setdefault(track[turn], []).append(drone)
            slot: dict[int, tuple[int, int]] = {}
            for members in groups.values():
                for i, drone in enumerate(members):
                    slot[drone] = (i, len(members))
            self.slots.append(slot)

        self.time = 0.0
        self.paused = False

    def moves(self, turn: int) -> list[tuple[int, str, str]]:
        """Drones that change zone/link during `turn` (turn-1 -> turn)."""
        if turn <= 0 or turn > self.max_turn:
            return []
        return [
            (drone, track[turn - 1], track[turn])
            for drone, track in self.tracks.items()
            if track[turn - 1] != track[turn]
        ]

    # ---------- playback controls ----------

    @property
    def finished(self) -> bool:
        return self.time >= self.max_turn

    @property
    def display_turn(self) -> int:
        """Turn whose moves are currently on screen."""
        return min(self.max_turn, max(0, math.ceil(self.time - 1e-9)))

    @property
    def speed(self) -> float:
        return SPEEDS[self.speed_index]

    def toggle_pause(self) -> None:
        if self.finished:
            self.restart()
        else:
            self.paused = not self.paused

    def restart(self) -> None:
        self.time = 0.0
        self.paused = False

    def step(self, delta: int) -> None:
        """Pause and snap to the previous / next whole turn."""
        if delta > 0:
            target: int = math.floor(self.time + 1e-9) + 1
        else:
            target = math.ceil(self.time - 1e-9) - 1
        self.time = float(max(0, min(self.max_turn, target)))
        self.paused = True

    def seek(self, turn: float) -> None:
        self.time = float(max(0, min(self.max_turn, round(turn))))
        self.paused = True

    def change_speed(self, delta: int) -> None:
        self.speed_index = max(0, min(len(SPEEDS) - 1, self.speed_index + delta))

    def update(self, dt: float) -> None:
        if self.paused:
            return
        self.anim += dt
        self.time = min(float(self.max_turn), self.time + dt * self.speed)

    # ---------- drawing ----------

    def anchor(self, name: str) -> tuple[float, float]:
        """Center of a zone, or middle of a link (drone in transit)."""
        coords: Any = self.coordinates[name]
        if "-" in name:
            (x1, y1), (x2, y2) = coords
            return ((x1 + x2) / 2, (y1 + y2) / 2)
        x, y = coords
        return (x + NODE / 2, y + NODE / 2)

    def sprite(self, size: int) -> Any:
        if size not in self._sprites:
            self._sprites[size] = pygame.transform.scale(
                self.base_img, (size, size)
            )
        return self._sprites[size]

    def label(self, drone: int) -> Any:
        if drone not in self._labels:
            text: str = f"D{drone}"
            shadow: Any = self.font.render(text, True, (0, 0, 0))
            front: Any = self.font.render(text, True, (255, 255, 255))
            surf: Any = pygame.Surface(
                (front.get_width() + 2, front.get_height() + 2),
                pygame.SRCALPHA
            )
            surf.blit(shadow, (2, 2))
            surf.blit(front, (0, 0))
            self._labels[drone] = surf
        return self._labels[drone]

    def draw(self, to_screen: Any) -> None:
        if not self.tracks:
            return

        k: int = min(int(self.time), self.max_turn)
        if k >= self.max_turn:
            k2, s = k, 0.0
        else:
            k2, s = k + 1, ease(self.time - k)

        win_w, win_h = self.window.get_size()
        items: list[tuple[float, int, float, float, float]] = []

        for drone, track in self.tracks.items():
            ax, ay = self.anchor(track[k])
            bx, by = self.anchor(track[k2])
            ia, na = self.slots[k][drone]
            ib, nb = self.slots[k2][drone]
            oax, oay = spread(ia, na)
            obx, oby = spread(ib, nb)

            x: float = lerp(ax + oax, bx + obx, s)
            y: float = lerp(ay + oay, by + oby, s)
            size: float = lerp(size_for(na), size_for(nb), s)
            bob: float = math.sin(self.anim * 4 + drone) * 3
            items.append((y, drone, x, y + bob, size))

        for _, drone, x, y, size in sorted(items):
            sx, sy = to_screen(x, y)
            if not (-80 < sx < win_w + 80 and -80 < sy < win_h + 80):
                continue
            px: int = int(size)
            self.window.blit(
                self.sprite(px),
                (int(sx - px / 2), int(sy - px / 2))
            )
            if px >= 40 or self.paused:
                label: Any = self.label(drone)
                self.window.blit(
                    label,
                    (int(sx - label.get_width() / 2),
                     int(sy - px / 2 - label.get_height() + 2))
                )
