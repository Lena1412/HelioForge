# src/cosmoview/app.py
from __future__ import annotations

"""cosmoview.app

Main pygame application loop for CosmoView.

CosmoView is a lightweight viewer for helioforge simulations. It focuses on
smooth rendering and simple interaction:
- pause / play,
- time scaling (faster/slower),
- zoom and pan,
- optional labels and an on-screen stats overlay.

The simulation itself is advanced using fixed-size substeps to keep motion
stable even when the time scale is high.
"""

import math
from dataclasses import dataclass, field

import pygame

from helioforge import CentralBody, SolarSystem, generate_planets, make_solar_system
from helioforge.simulation import Simulation

from .controls import IconButton, draw_tooltip
from .scaling import ScaleModel
from .ui import StatsPanel


@dataclass
class ViewState:
    """Viewer state that controls how the scene is rendered and advanced.

    Attributes:
        paused: Whether simulation stepping is paused.
        time_scale: Multiplier converting real seconds to simulated seconds.
        zoom: Zoom factor applied to the world-to-screen scaling.
        cam_px: Camera center in screen pixels (used as the origin of the world).
        show_labels: Whether planet names are drawn.
        show_stats: Whether the stats overlay is drawn.
    """

    paused: bool = False
    time_scale: float = 20000.0
    zoom: float = 1.0
    cam_px: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0.0, 0.0))
    show_labels: bool = True
    show_stats: bool = True


def _build_demo_system(mode: str) -> SolarSystem:
    """Create a demo SolarSystem for a given mode.

    Args:
        mode: "solar" to load an approximate Solar System preset, otherwise a
            deterministic generated system is used.

    Returns:
        A `SolarSystem` suitable for visualization.
    """
    if mode == "solar":
        sun, planets = make_solar_system()
        return SolarSystem(central_body=sun, planets=planets)

    star = CentralBody(name="DemoStar", mass_kg=1.2e30, radius_m=7.0e8, luminosity_w=2.0e26)
    planets = generate_planets(star, 8, seed=123, inner_au=0.3, outer_au=40.0)
    return SolarSystem(central_body=star, planets=planets)


def _make_font() -> pygame.font.Font:
    """Create a UI font with a small fallback list."""
    return pygame.font.SysFont(["Inter", "Segoe UI", "DejaVu Sans", "Arial", "consolas"], 16)


def run(*, width: int = 1100, height: int = 800, fps_limit: int = 60, mode: str = "solar") -> None:
    """Run the CosmoView pygame window.

    Args:
        width: Window width in pixels.
        height: Window height in pixels.
        fps_limit: Target frame rate.
        mode: Demo system mode ("solar" or "random").

    Notes:
        The rendering pipeline uses a higher-resolution offscreen surface
        (`render_scale`) and then downsamples via `smoothscale`. This acts like
        a simple supersampling anti-aliasing pass and helps motion appear
        smoother (especially for thin orbit lines).
    """
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption("CosmoView")
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    ui_font = _make_font()
    stats_panel = StatsPanel(ui_font)

    scale = ScaleModel(pixels_per_log_unit=220.0, base_m=8.0e9)

    view = ViewState()
    view.cam_px = pygame.Vector2(width / 2, height / 2)

    def reset_sim() -> Simulation:
        """Build a fresh simulation instance for the current mode."""
        return Simulation(_build_demo_system(mode))

    sim = reset_sim()

    def do_reset() -> None:
        """Reset the current simulation (UI action)."""
        nonlocal sim
        sim = reset_sim()

    def slower() -> None:
        """Decrease the simulation time scale (UI action)."""
        view.time_scale = max(0.1, view.time_scale / 1.25)

    def faster() -> None:
        """Increase the simulation time scale (UI action)."""
        view.time_scale *= 1.25

    def zoom_out() -> None:
        """Zoom out (UI action)."""
        view.zoom = max(0.1, view.zoom / 1.1)

    def zoom_in() -> None:
        """Zoom in (UI action)."""
        view.zoom *= 1.1

    def toggle_labels() -> None:
        """Toggle planet name labels (UI action)."""
        view.show_labels = not view.show_labels

    def toggle_stats() -> None:
        """Toggle the stats overlay (UI action)."""
        view.show_stats = not view.show_stats

    def toggle_pause() -> None:
        """Toggle simulation pause state (UI action)."""
        view.paused = not view.paused

    bottom_h = 78
    bar_rect = pygame.Rect(10, height - bottom_h + 10, width - 20, bottom_h - 20)

    btn = 44
    gap = 10
    pad = 14

    left_kinds = ["stop", "labels", "stats"]
    center_kinds = ["rew", "playpause", "ff"]
    right_kinds = ["zoom_out", "zoom_in"]

    right_w = len(right_kinds) * btn + (len(right_kinds) - 1) * gap
    center_w = len(center_kinds) * btn + (len(center_kinds) - 1) * gap

    left_x = bar_rect.x + pad
    right_x = bar_rect.right - pad - right_w
    center_x = bar_rect.centerx - center_w // 2
    y = bar_rect.y + (bar_rect.height - btn) // 2

    def rects_from(x0: int, n: int) -> list[pygame.Rect]:
        """Generate `n` button rects in a row starting at x0."""
        rs = []
        x = x0
        for _ in range(n):
            rs.append(pygame.Rect(x, y, btn, btn))
            x += btn + gap
        return rs

    left_rects = rects_from(left_x, len(left_kinds))
    center_rects = rects_from(center_x, len(center_kinds))
    right_rects = rects_from(right_x, len(right_kinds))

    buttons: list[IconButton] = [
        IconButton(left_rects[0], "stop", do_reset, "Reset simulation", shortcut_hint="R"),
        IconButton(left_rects[1], "labels", toggle_labels, "Toggle labels", shortcut_hint="S"),
        IconButton(left_rects[2], "stats", toggle_stats, "Toggle statistics", shortcut_hint="T"),
        IconButton(center_rects[0], "rew", slower, "Slower", shortcut_hint="-"),
        IconButton(center_rects[1], "pause", toggle_pause, "Play / Pause", shortcut_hint="SPACE"),
        IconButton(center_rects[2], "ff", faster, "Faster", shortcut_hint="+"),
        IconButton(right_rects[0], "zoom_out", zoom_out, "Zoom out", shortcut_hint="Wheel down"),
        IconButton(right_rects[1], "zoom_in", zoom_in, "Zoom in", shortcut_hint="Wheel up"),
    ]

    # Maximum simulated seconds per substep. Large time_scale values can
    # otherwise cause very large dt jumps which look like teleportation.
    max_sim_step = 90000.0
    max_substeps = 240

    # Render to an offscreen surface with a higher resolution and downsample
    # for smoother orbit lines and circles.
    render_scale = 2
    world = pygame.Surface((width * render_scale, height * render_scale)).convert()

    bg = (10, 10, 18)

    running = True
    while running:
        dt_real = clock.tick(fps_limit) / 1000.0
        fps = clock.get_fps()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.handle_event(event, mouse_pos):
                        break

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    toggle_pause()
                elif event.key == pygame.K_r:
                    do_reset()
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    faster()
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    slower()
                elif event.key == pygame.K_s:
                    toggle_labels()
                elif event.key == pygame.K_t:
                    toggle_stats()

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    zoom_in()
                elif event.y < 0:
                    zoom_out()

        # Simple camera panning with arrow keys (screen-space).
        keys = pygame.key.get_pressed()
        pan_speed = 400.0 * dt_real
        if keys[pygame.K_LEFT]:
            view.cam_px.x += pan_speed
        if keys[pygame.K_RIGHT]:
            view.cam_px.x -= pan_speed
        if keys[pygame.K_UP]:
            view.cam_px.y += pan_speed
        if keys[pygame.K_DOWN]:
            view.cam_px.y -= pan_speed

        if not view.paused:
            dt_sim_total = dt_real * view.time_scale
            if dt_sim_total > 0:
                # Substepping prevents very large dt values from skipping too far
                # around an orbit in a single frame.
                n = max(1, int(math.ceil(dt_sim_total / max_sim_step)))
                if n > max_substeps:
                    n = max_substeps
                dt_sub = dt_sim_total / n
                for _ in range(n):
                    sim.step(dt_sub)

        world.fill(bg)

        center = pygame.Vector2(view.cam_px.x * render_scale, view.cam_px.y * render_scale)

        sun_r_px = ScaleModel.clamp_radius_px(10 * view.zoom, 6, 18) * render_scale
        pygame.draw.circle(world, (255, 210, 80), (int(center.x), int(center.y)), int(sun_r_px))

        orbit_width = max(1, render_scale)

        for p in sim.system.planets:
            orbit_r_px = max(1.0, scale.meters_to_pixels_radius(p.distance_m, view.zoom)) * render_scale
            pygame.draw.circle(world, (40, 40, 65), (int(center.x), int(center.y)), int(orbit_r_px), width=orbit_width)

            # Convert the planet's model-space position to a unit direction and
            # then scale by the orbit radius in pixels.
            x_m, y_m = p.position_m()
            r_m = math.hypot(x_m, y_m)
            ux, uy = (x_m / r_m, y_m / r_m) if r_m > 0 else (0.0, 0.0)

            px = center.x + ux * orbit_r_px
            py = center.y + uy * orbit_r_px

            pr = ScaleModel.clamp_radius_px(2.0 * view.zoom, 2, 8) * render_scale
            color = {
                "rocky": (200, 200, 200),
                "gas_giant": (210, 170, 120),
                "ice_giant": (140, 180, 220),
                "dwarf": (180, 180, 140),
            }.get(p.kind, (200, 200, 200))

            pygame.draw.circle(world, color, (int(px), int(py)), int(pr))

        pygame.transform.smoothscale(world, (width, height), screen)

        if view.show_labels:
            center_ui = view.cam_px
            for p in sim.system.planets:
                orbit_r_px = max(1.0, scale.meters_to_pixels_radius(p.distance_m, view.zoom))
                x_m, y_m = p.position_m()
                r_m = math.hypot(x_m, y_m)
                ux, uy = (x_m / r_m, y_m / r_m) if r_m > 0 else (0.0, 0.0)

                px = center_ui.x + ux * orbit_r_px
                py = center_ui.y + uy * orbit_r_px

                label = ui_font.render(p.name, True, (220, 220, 220))
                screen.blit(label, (int(px + 8), int(py - 10)))

        if view.show_stats:
            stats_panel.draw(
                screen,
                paused=view.paused,
                sim_time_s=sim.time_s,
                time_scale=view.time_scale,
                zoom=view.zoom,
                fps=fps,
                show_labels=view.show_labels,
                top_left=(14, 14),
            )

        pygame.draw.rect(screen, (16, 16, 24), bar_rect, border_radius=16)
        pygame.draw.rect(screen, (70, 74, 102), bar_rect, width=2, border_radius=16)

        hovered_tooltip: str | None = None
        for b in buttons:
            # Swap the icon for the central play/pause button based on state.
            if b.kind in ("play", "pause"):
                b.kind = "pause" if not view.paused else "play"
                b.toggled = view.paused
            if b.kind == "labels":
                b.toggled = view.show_labels
            if b.kind == "stats":
                b.toggled = view.show_stats

            b.draw(screen, ui_font, mouse_pos)
            if hovered_tooltip is None and b.is_hovered(mouse_pos):
                hovered_tooltip = f"{b.tooltip}\nShortcut: {b.shortcut_hint}" if b.shortcut_hint else b.tooltip

        if hovered_tooltip:
            draw_tooltip(screen, ui_font, hovered_tooltip, mouse_pos)

        pygame.display.flip()

    pygame.quit()
