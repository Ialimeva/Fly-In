import pygame
from .engine import Engine
from .renderer import GraphRenderer, Camera, Utils, BackgroundRenderer, DronesRenderer
from ..models import Hub, Connection
from typing import Any


class Visual:
    def __init__(
        self,
        actions_per_turn: dict[int, Any],
        nodes: dict[str, Hub],
        edges: dict[str, Connection],
    ) -> None:
        pygame.init()
        info: Any = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h
        self.window: Any = pygame.display.set_mode(
            (self.width, self.height)
        )

        self.actions_per_turn: dict[int, Any] = actions_per_turn
        self.nodes: dict[str, Hub] = nodes
        self.edges: dict[str, Connection] = edges

        self.utils: Utils = Utils()
        self.graph_renderer: GraphRenderer = GraphRenderer(self.window, self.nodes, self.edges, self.utils)
        self.background_renderer: BackgroundRenderer = BackgroundRenderer(self.utils, self.window)
        self.graph_buffer, self.coordinates = self.graph_renderer.draw_graph()
        self.drones_renderer: DronesRenderer = DronesRenderer(self.actions_per_turn, self.coordinates, self.graph_buffer)
        self.camera: Camera = Camera(self.window, self.graph_buffer)
        self.engine: Engine = Engine(self.graph_renderer, self.background_renderer, self.drones_renderer, self.camera)


    def start(self) -> None:
        self.engine.event_loop()