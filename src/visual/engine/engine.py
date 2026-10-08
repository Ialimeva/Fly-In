import pygame
from typing import Any
from ..renderer import (
    GraphRenderer, Camera, BackgroundRenderer, DronesRenderer, Hud
)


class Engine:
    def __init__(
        self,
        graph_renderer: GraphRenderer,
        background_renderer: BackgroundRenderer,
        drone_renderer: DronesRenderer,
        camera: Camera,
        hud: Hud,
        window: Any
    ) -> None:
        self.graph_renderer: GraphRenderer = graph_renderer
        self.background_renderer: BackgroundRenderer = background_renderer
        self.drone_renderer: DronesRenderer = drone_renderer
        self.camera: Camera = camera
        self.hud: Hud = hud
        self.window: Any = window

    def quit(self) -> None:
        pygame.quit()
        raise SystemExit

    def handle_key(self, key: int) -> None:
        d: DronesRenderer = self.drone_renderer
        if key == pygame.K_ESCAPE:
            self.quit()
        elif key in (pygame.K_SPACE, pygame.K_p):
            d.toggle_pause()
        elif key in (pygame.K_PERIOD, pygame.K_RIGHTBRACKET):
            d.step(1)
        elif key in (pygame.K_COMMA, pygame.K_LEFTBRACKET):
            d.step(-1)
        elif key == pygame.K_r:
            d.restart()
        elif key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
            d.change_speed(1)
        elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            d.change_speed(-1)

    def event_loop(self) -> None:
        pygame.display.set_caption("FLY-IN")
        clock: Any = pygame.time.Clock()
        cam_x, cam_y = (0, 0)
        dragging: bool = False

        while True:
            dt: float = clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    dragging = not self.hud.handle_click(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging = False
                elif event.type == pygame.MOUSEMOTION and dragging:
                    cam_x -= event.rel[0]
                    cam_y -= event.rel[1]

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                cam_y -= self.camera.speed

            if keys[pygame.K_DOWN]:
                cam_y += self.camera.speed

            if keys[pygame.K_LEFT]:
                cam_x -= self.camera.speed

            if keys[pygame.K_RIGHT]:
                cam_x += self.camera.speed

            self.drone_renderer.update(dt)

            self.background_renderer.animate()
            cam_x, cam_y = self.camera.present(cam_x, cam_y)
            to_screen: Any = self.camera.world_to_screen
            self.graph_renderer.draw_overlay(
                to_screen, self.drone_renderer.anim
            )
            self.drone_renderer.draw(to_screen)
            self.hud.draw()

            pygame.display.flip()
