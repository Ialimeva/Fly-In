import pygame
from typing import Any
from ..renderer import GraphRenderer, Camera, BackgroundRenderer


class Engine:
    def __init__(
        self,
        graph_renderer: GraphRenderer,
        background_renderer: BackgroundRenderer,
        camera: Camera
    ) -> None:
        self.graph_renderer: GraphRenderer = graph_renderer
        self.background_renderer: BackgroundRenderer = background_renderer
        self.camera: Camera = camera

    def event_loop(self) -> None:
        pygame.display.set_caption("FLY-IN")
        cam_x, cam_y = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            self.background_renderer.animate()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                cam_y -= self.camera.speed

            if keys[pygame.K_DOWN]:
                cam_y += self.camera.speed

            if keys[pygame.K_LEFT]:
                cam_x -= self.camera.speed

            if keys[pygame.K_RIGHT]:
                cam_x += self.camera.speed

            self.camera.present(cam_x, cam_y)
            pygame.display.flip()
                # if event.type == pygame.KEYUP:
                #     key=pygame.key.name(event.key)
                #     print(key, "released")