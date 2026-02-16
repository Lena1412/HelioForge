# controls for the UI
# a button class and a tooltip for the pygame app
# stored in the ui file before
# separated to make the code structure cleaner but more complex


# src/cosmoview/controls.py
from __future__ import annotations

"""cosmoview.controls

UI control primitives used by the CosmoView pygame viewer.

This module contains:
- a small icon-button widget used for the bottom control bar,
- tooltip rendering helpers.

The goal is to keep UI elements lightweight and dependency-free while still
being pleasant to use in a realtime render loop.
"""

from dataclasses import dataclass
from typing import Callable, Optional, Tuple

import pygame


@dataclass
class IconButton:
    """A clickable icon-style button.

    The button is purely immediate-mode: it holds a rectangle and a click
    callback, and it draws itself each frame based on current hover/toggle
    state. It does not manage global UI focus; the app decides which buttons
    receive input.

    Attributes:
        rect: Screen-space rectangle for hit testing and drawing.
        kind: Icon identifier (e.g., "play", "pause", "ff"). Used by `_draw_icon`.
        on_click: Callback invoked when the button is left-clicked.
        tooltip: Tooltip text shown on hover.
        shortcut_hint: Optional keyboard shortcut hint displayed in tooltip.
        enabled: Whether the button is interactive.
        toggled: Whether the button is in an "active" visual state.
    """

    rect: pygame.Rect
    kind: str
    on_click: Callable[[], None]
    tooltip: str
    shortcut_hint: Optional[str] = None
    enabled: bool = True
    toggled: bool = False

    def is_hovered(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check whether the mouse is hovering over the button.

        Args:
            mouse_pos: Current mouse position in screen pixels.

        Returns:
            True if the button is enabled and the mouse is inside `rect`.
        """
        return self.enabled and self.rect.collidepoint(mouse_pos)

    def handle_event(
        self, event: pygame.event.Event, mouse_pos: Tuple[int, int]
    ) -> bool:
        """Handle a single pygame event for this button.

        The only handled interaction is a left mouse button press when the
        cursor is inside the button rectangle.

        Args:
            event: A pygame event from the event queue.
            mouse_pos: Current mouse position in screen pixels.

        Returns:
            True if the event was consumed (click happened), otherwise False.
        """
        if not self.enabled:
            return False
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(mouse_pos)
        ):
            self.on_click()
            return True
        return False

    def draw(
        self, screen: pygame.Surface, font: pygame.font.Font, mouse_pos: Tuple[int, int]
    ) -> None:
        """Draw the button to the given surface.

        Args:
            screen: Target surface to draw onto.
            font: Font used as a fallback for unknown icon kinds.
            mouse_pos: Current mouse position in screen pixels.
        """
        hovered = self.is_hovered(mouse_pos)

        base = (28, 30, 44)
        border = (70, 74, 102)
        hover = (42, 46, 70)
        active = (52, 56, 84)
        fg = (238, 238, 245)
        disabled = (130, 130, 140)

        bg = base
        if self.toggled:
            bg = active
        if hovered:
            bg = hover if not self.toggled else (64, 68, 104)

        # Subtle shadow improves legibility on dark backgrounds.
        shadow = self.rect.move(0, 2)
        pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=12)
        pygame.draw.rect(screen, bg, self.rect, border_radius=12)
        pygame.draw.rect(screen, border, self.rect, width=2, border_radius=12)

        color = fg if self.enabled else disabled
        self._draw_icon(screen, color, font)

    def _draw_icon(
        self,
        screen: pygame.Surface,
        color: Tuple[int, int, int],
        font: pygame.font.Font,
    ) -> None:
        """Render an icon matching `self.kind`.

        This intentionally avoids loading external icon assets. Each icon is a
        tiny vector drawing composed of pygame primitives.

        Args:
            screen: Target surface to draw onto.
            color: Foreground color for the icon.
            font: Used only as a fallback to render raw text for unknown kinds.
        """
        cx, cy = self.rect.centerx, self.rect.centery
        w, h = self.rect.width, self.rect.height
        s = min(w, h)

        # NOTE: Icon geometry is derived from the button size `s` so that icons
        # remain visually consistent as UI scale changes.
        if self.kind == "play":
            size = int(s * 0.34)
            pts = [
                (cx - size // 2, cy - size),
                (cx - size // 2, cy + size),
                (cx + size, cy),
            ]
            pygame.draw.polygon(screen, color, pts)
            return

        if self.kind == "pause":
            bw = int(s * 0.16)
            bh = int(s * 0.50)
            gap = int(s * 0.10)
            r1 = pygame.Rect(cx - gap // 2 - bw, cy - bh // 2, bw, bh)
            r2 = pygame.Rect(cx + gap // 2, cy - bh // 2, bw, bh)
            pygame.draw.rect(screen, color, r1, border_radius=3)
            pygame.draw.rect(screen, color, r2, border_radius=3)
            return

        if self.kind == "ff":
            size = int(s * 0.26)
            off = int(s * 0.08)
            pts1 = [(cx - off, cy - size), (cx - off, cy + size), (cx + size, cy)]
            pts2 = [
                (cx - size - off, cy - size),
                (cx - size - off, cy + size),
                (cx - off, cy),
            ]
            pygame.draw.polygon(screen, color, pts2)
            pygame.draw.polygon(screen, color, pts1)
            return

        if self.kind == "rew":
            size = int(s * 0.26)
            off = int(s * 0.08)
            pts1 = [(cx + off, cy - size), (cx + off, cy + size), (cx - size, cy)]
            pts2 = [
                (cx + size + off, cy - size),
                (cx + size + off, cy + size),
                (cx + off, cy),
            ]
            pygame.draw.polygon(screen, color, pts2)
            pygame.draw.polygon(screen, color, pts1)
            return

        if self.kind == "stop":
            size = int(s * 0.34)
            r = pygame.Rect(cx - size, cy - size, 2 * size, 2 * size)
            pygame.draw.rect(screen, color, r, border_radius=4)
            return

        if self.kind == "labels":
            bw = int(s * 0.58)
            bh = int(s * 0.34)
            r = pygame.Rect(cx - bw // 2, cy - bh // 2, bw, bh)
            pygame.draw.rect(screen, color, r, width=2, border_radius=6)
            hole = pygame.Rect(
                r.x + int(bw * 0.12),
                r.y + int(bh * 0.35),
                int(bh * 0.18),
                int(bh * 0.18),
            )
            pygame.draw.ellipse(screen, color, hole, width=2)
            return

        if self.kind == "stats":
            base_y = cy + int(s * 0.20)
            bw = int(s * 0.12)
            gap = int(s * 0.10)
            heights = [int(s * 0.22), int(s * 0.36), int(s * 0.28)]
            start_x = cx - (3 * bw + 2 * gap) // 2
            for i, hh in enumerate(heights):
                r = pygame.Rect(start_x + i * (bw + gap), base_y - hh, bw, hh)
                pygame.draw.rect(screen, color, r, border_radius=3)
            return

        if self.kind == "zoom_in" or self.kind == "zoom_out":
            radius = int(s * 0.20)
            center = (cx - int(s * 0.06), cy - int(s * 0.04))
            pygame.draw.circle(screen, color, center, radius, width=2)
            hx1 = center[0] + int(radius * 0.75)
            hy1 = center[1] + int(radius * 0.75)
            hx2 = hx1 + int(s * 0.18)
            hy2 = hy1 + int(s * 0.18)
            pygame.draw.line(screen, color, (hx1, hy1), (hx2, hy2), width=3)

            line_w = int(s * 0.18)
            pygame.draw.line(
                screen,
                color,
                (center[0] - line_w // 2, center[1]),
                (center[0] + line_w // 2, center[1]),
                width=2,
            )
            if self.kind == "zoom_in":
                pygame.draw.line(
                    screen,
                    color,
                    (center[0], center[1] - line_w // 2),
                    (center[0], center[1] + line_w // 2),
                    width=2,
                )
            return

        # Fallback: render the kind string as text (useful during development).
        text = font.render(self.kind, True, color)
        screen.blit(text, (cx - text.get_width() // 2, cy - text.get_height() // 2))


def draw_tooltip(
    screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    mouse_pos: Tuple[int, int],
) -> None:
    """Draw a tooltip bubble near the mouse cursor.

    The tooltip is kept on-screen by clamping its rect to the current window
    size, which avoids partially clipped tooltips near edges.

    Args:
        screen: Target surface to draw onto.
        font: Font used to render the tooltip text.
        text: Tooltip text. Newlines are supported.
        mouse_pos: Current mouse position in screen pixels.
    """
    padding = 10
    lines = text.split("\n")
    rendered = [font.render(line, True, (240, 240, 240)) for line in lines]

    w = max(s.get_width() for s in rendered) + 2 * padding
    h = sum(s.get_height() for s in rendered) + 2 * padding + (len(rendered) - 1) * 3

    x, y = mouse_pos
    x += 16
    y += 16

    # Clamp tooltip to window bounds (small margin for nicer look).
    sw, sh = screen.get_size()
    if x + w > sw:
        x = sw - w - 10
    if y + h > sh:
        y = sh - h - 50

    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, (16, 16, 24), rect, border_radius=12)
    pygame.draw.rect(screen, (80, 84, 120), rect, width=2, border_radius=12)

    cy = y + padding
    for surf in rendered:
        screen.blit(surf, (x + padding, cy))
        cy += surf.get_height() + 3
