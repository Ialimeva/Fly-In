import pygame
from typing import Any
from .utils import Utils
from ...models import Hub, Connection


class GraphRenderer:
    def __init__(
        self,
        window: Any,
        nodes: dict[str, Hub],
        edges: dict[str, Connection],
        utils: Utils
    ) -> None:
        self.window = window
        self.window_w, self.window_h = self.window.get_rect().size
        self.center_w, self.center_h = (self.window_w // 2, self.window_h // 2)

        self.nodes: dict[str, Hub] = nodes
        self.edges: dict[str, Connection] = edges
        self.utils: Utils = utils

        self.edge_w: int = 250
        self.edge_h: int = 50
        self.label_h: int = 24

        self.zones: dict[str, Any] = {}
        for zone in ("normal", "priority", "restricted", "blocked"):
            raw_img = pygame.image.load(
                f"src/visual/assets/zones/{zone}.png"
            ).convert_alpha()

            w, h = raw_img.get_rect().size
            self.zones[zone] = self.utils.scale_img(
                raw_img, (w, h)
            )

        self.node_w, self.node_h = (64, 64)
        self.xs: list[int] = [node.x for _, node in self.nodes.items()]
        self.ys: list[int] = [node.y for _, node in self.nodes.items()]

        self.font: Any = pygame.font.Font(None, 22)
        self.coordinates: dict[str, Any] = {}
        self.rainbow_nodes: list[str] = []

    def graph_size(self) -> tuple[int, int]:
        graph_w: int = (max(self.xs) - min(self.xs)) * (self.node_w + self.edge_w) + self.node_w
        graph_y: int = (max(self.ys) - min(self.ys)) * (self.node_h + self.edge_h) + self.node_h + self.label_h

        return (graph_w, graph_y)

    def make_label(self, name: str, node: Hub) -> Any:
        text: str = name
        if node.type == "start_hub":
            text += " (start)"
        elif node.type == "end_hub":
            text += " (end)"
        elif node.metadata.max_drones > 1:
            text += f" [{node.metadata.max_drones}]"

        shadow: Any = self.font.render(text, True, (0, 0, 0))
        front: Any = self.font.render(text, True, (255, 255, 255))
        label: Any = pygame.Surface(
            (front.get_width() + 2, front.get_height() + 2),
            pygame.SRCALPHA
        )
        label.blit(shadow, (2, 2))
        label.blit(front, (0, 0))

        return label

    def draw_graph(self) -> Any:
        graph_w, graph_y = self.graph_size()
        buffer: Any = pygame.Surface(
            (graph_w, graph_y),
            pygame.SRCALPHA
        )

        for edge_name, edge in self.edges.items():
            node1 = self.nodes[edge.name1]
            node2= self.nodes[edge.name2]

            start_x = (node1.x - min(self.xs)) * (self.node_w + self.edge_w) + (self.node_w // 2)
            start_y = (node1.y - min(self.ys)) * (self.node_h + self.edge_h) + (self.node_h // 2)

            end_x = (node2.x - min(self.xs)) * (self.node_w + self.edge_w) + (self.node_w // 2)
            end_y = (node2.y - min(self.ys)) * (self.node_h + self.edge_h) + (self.node_h // 2)

            self.coordinates[edge_name] = [(start_x, start_y), (end_x, end_y)]
            pygame.draw.line(buffer, (255, 255, 255), (start_x, start_y), (end_x, end_y), 5)

        for node_name, node in self.nodes.items():
            x: int = (node.x - min(self.xs)) * (self.node_w + self.edge_w)
            y: int = (node.y - min(self.ys)) * (self.node_h + self.edge_h)

            self.coordinates[node_name] = (x, y)

            sprite: Any = self.zones[node.metadata.zone]
            color_name: str | None = node.metadata.color
            color: Any = self.utils.parse_color(color_name)

            if color_name and color_name.lower() == "rainbow":
                self.rainbow_nodes.append(node_name)
            elif color is not None:
                sprite = self.utils.tint(sprite, color)

            buffer.blit(sprite, (x, y))

            if color is not None:
                frame = pygame.Rect(x, y, self.node_w, self.node_h)
                # White underlay keeps dark colors visible on dark frames.
                pygame.draw.rect(buffer, (255, 255, 255), frame, 6, border_radius=16)
                pygame.draw.rect(buffer, color, frame.inflate(-2, -2), 4, border_radius=15)

            label: Any = self.make_label(node_name, node)
            label_x: int = x + self.node_w // 2 - label.get_width() // 2
            label_x = max(0, min(label_x, graph_w - label.get_width()))
            buffer.blit(label, (label_x, y + self.node_h + 2))

        return (buffer, self.coordinates)

    def draw_overlay(self, to_screen: Any, clock: float) -> None:
        """Animated frames for color=rainbow hubs, drawn straight on screen."""
        for name in self.rainbow_nodes:
            x, y = self.coordinates[name]
            sx, sy = to_screen(x, y)
            color: Any = pygame.Color(0, 0, 0)
            color.hsva = ((clock * 120) % 360, 85, 100, 100)
            frame = pygame.Rect(int(sx), int(sy), self.node_w, self.node_h)
            pygame.draw.rect(self.window, (255, 255, 255), frame, 6, border_radius=16)
            pygame.draw.rect(self.window, color, frame.inflate(-2, -2), 4, border_radius=15)
