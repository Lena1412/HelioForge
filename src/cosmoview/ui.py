# src/cosmoview/ui.py
from __future__ import annotations

import pygame


class StatsPanel:
    def __init__(self, font: pygame.font.Font):
        self.font = font

    def draw(
        self,
        screen: pygame.Surface,
        *,
        paused: bool,
        sim_time_s: float,
        time_scale: float,
        zoom: float,
        fps: float,
        show_labels: bool,
        top_left: tuple[int, int] = (14, 14),
    ) -> None:
        state = "Paused" if paused else "Running"
        lines = [
            state,
            f"t: {sim_time_s:,.0f} s",
            f"speed: x{time_scale:,.0f}",
            f"zoom: {zoom:.2f}",
            f"labels: {'on' if show_labels else 'off'}",
            f"fps: {fps:.0f}",
        ]

        rendered = [self.font.render(line, True, (235, 235, 242)) for line in lines]
        padding_x, padding_y = 12, 10
        gap = 4

        w = max(s.get_width() for s in rendered) + 2 * padding_x
        h = sum(s.get_height() for s in rendered) + 2 * padding_y + gap * (len(rendered) - 1)

        x, y = top_left
        rect = pygame.Rect(x, y, w, h)

        pygame.draw.rect(screen, (18, 18, 28), rect, border_radius=14)
        pygame.draw.rect(screen, (70, 74, 102), rect, width=2, border_radius=14)

        cy = y + padding_y
        for surf in rendered:
            screen.blit(surf, (x + padding_x, cy))
            cy += surf.get_height() + gap
