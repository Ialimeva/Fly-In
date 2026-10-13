"""
Entry point of the visual part of the pipeline.

This module creates the pygame window and builds every renderer
needed to display the simulation: the animated background, the
graph, the drones, the camera and the playback controls.

Extracted class:
    Visual: Build and start the visualization.
"""
import pygame
from .engine import Engine
from .renderer import (
    GraphRenderer,
    Camera,
    Utils,
    BackgroundRenderer,
    DronesRenderer,
    Hud
)
from models import Hub, Connection
from typing import Any


class Visual:
    """
    Build and start the visualization.

    Attributes:
        width: Screen width.
        height: Screen height.
        padding_w: Horizontal space kept between the window and
        the screen size.
        padding_h: Vertical space kept between the window and
        the screen size.
        window: Pygame window, the screen size minus the padding.
        actions_per_turn: Drones actions organized by turn, filled
        by the simulation after the visual is created.
        nodes: Zones of the map.
        edges: Links of the map.
        utils: Image helpers.
        graph_renderer: Draw the graph and compute zones coordinates.
        background_renderer: Animate the background images.
        graph_buffer: Surface where the whole graph is drawn.
        coordinates: Position of each zone and link in the buffer.
        drones_renderer: Build the drones timeline and draw drones.
        camera: Show the part of the graph buffer in the window.
        hud: Playback controls drawn above the animation.
        engine: Event loop that updates and draws everything.
    """
    def __init__(
        self,
        actions_per_turn: dict[int, Any],
        nodes: dict[str, Hub],
        edges: dict[str, Connection],
    ) -> None:
        pygame.init()
        info: Any = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h
        self.padding_w, self.padding_h = (100, 100)
        self.window: Any = pygame.display.set_mode(
            (self.width - self.padding_w, self.height - self.padding_h)
        )

        self.actions_per_turn: dict[int, Any] = actions_per_turn
        self.nodes: dict[str, Hub] = nodes
        self.edges: dict[str, Connection] = edges

        self.utils: Utils = Utils()
        self.graph_renderer: GraphRenderer = GraphRenderer(
            self.window,
            self.nodes,
            self.edges,
            self.utils
        )
        self.background_renderer: BackgroundRenderer = BackgroundRenderer(
            self.utils,
            self.window
        )
        self.graph_buffer, self.coordinates = self.graph_renderer.draw_graph()
        self.drones_renderer: DronesRenderer = DronesRenderer(
            self.actions_per_turn,
            self.coordinates,
            self.window,
            self.utils
        )
        self.camera: Camera = Camera(self.window, self.graph_buffer)
        self.hud: Hud = Hud(self.window, self.drones_renderer)
        self.engine: Engine = Engine(
            self.graph_renderer,
            self.background_renderer,
            self.drones_renderer,
            self.camera,
            self.hud,
            self.window
        )

    def start(self) -> None:
        """Build the drones timeline then start the event loop."""
        self.drones_renderer.build_timeline()
        self.engine.event_loop()
