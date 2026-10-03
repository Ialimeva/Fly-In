import pygame
from typing import Any
from .utils import Utils
from ...models import Hub, Connection


class GraphRenderer:
    def __init__(
        self,
        window: Any,
        nodes: dict[str, Hub],
        edges: dict[str, Connection]
    ) -> None:
        self.window = window
        self.window_w, self.window_h = self.window.get_rect().size
        self.center_w, self.center_h = (self.window_w // 2, self.window_h // 2)

        self.nodes: dict[str, Hub] = nodes
        self.edges: dict[str, Connection] = edges
        self.utils: Utils = Utils()

        self.edge_w: int = 250
        self.edge_h: int = 50

        raw_img: Any = pygame.image.load(
            "src/visual/assets/island.png"
        ).convert_alpha()
        w, h = raw_img.get_rect().size
        scaled_img: Any = self.utils.scale_img(raw_img, (w // 7, h // 7))

        self.node_img = self.utils.crop_img(scaled_img)
        self.node_w, self.node_h = self.node_img.get_rect().size
        self.xs: list[int] = [node.x for _, node in self.nodes.items()]
        self.ys: list[int] = [node.y for _, node in self.nodes.items()]

    def graph_size(self) -> tuple[int, int]:
        graph_w: int = (max(self.xs) - min(self.xs)) * (self.node_w + self.edge_w) + self.node_w
        graph_y: int = (max(self.ys) - min(self.ys)) * (self.node_h + self.edge_h) + self.node_h

        return (graph_w, graph_y)

    def draw_graph(self) -> Any:
        graph_w, graph_y = self.graph_size()
        buffer: Any = pygame.Surface(
            (graph_w, graph_y),
            pygame.SRCALPHA
        )

        for _, edge in self.edges.items():
            node1 = self.nodes[edge.name1]
            node2= self.nodes[edge.name2]

            start_x = (node1.x - min(self.xs)) * (self.node_w + self.edge_w) + (self.node_w // 2)
            start_y = (node1.y - min(self.ys)) * (self.node_h + self.edge_h) + (self.node_h // 2)

            end_x = (node2.x - min(self.xs)) * (self.node_w + self.edge_w) + (self.node_w // 2)
            end_y = (node2.y - min(self.ys)) * (self.node_h + self.edge_h) + (self.node_h // 2)

            pygame.draw.line(buffer, (255, 255, 255), (start_x, start_y), (end_x, end_y), 5)

        for _, node in self.nodes.items():
            x: int = (node.x - min(self.xs)) * (self.node_w + self.edge_w)
            y: int = (node.y - min(self.ys)) * (self.node_h + self.edge_h)

            buffer.blit(self.node_img, (x, y))

        return (buffer)