"""
Plantas vs Zombies - Lawn Board (5 Rows x 8 Columns)
Handles grid coordinates, planting logic, lawnmowers, and visual lawn rendering.
"""

import pygame
from constants import (
    GRID_ROWS, GRID_COLS, CELL_WIDTH, CELL_HEIGHT, GRID_START_X, GRID_START_Y,
    COLOR_GRASS_LIGHT, COLOR_GRASS_DARK, COLOR_PATIO, COLOR_PATIO_DARK, COLOR_SIDEWALK,
    SCREEN_WIDTH, SCREEN_HEIGHT, ZOMBIE_ALARM_X, ZOMBIE_LOSE_X,
    PLANT_SUNFLOWER, PLANT_PEASHOOTER, PLANT_WALLNUT, PLANT_POTATOMINE
)
from entities import Sunflower, Peashooter, Wallnut, PotatoMine, Lawnmower, Particle
from sprites import SpriteCache

class Board:
    def __init__(self):
        # 5 rows x 8 columns grid: grid[row][col] = Plant or None
        self.rows = GRID_ROWS
        self.cols = GRID_COLS
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        
        # 5 Lawnmowers, one for each row
        self.lawnmowers = [Lawnmower(r) for r in range(self.rows)]
        
        # Pre-rendered lawn surface for top performance
        self.lawn_surface = self._render_lawn_background()

    def _render_lawn_background(self):
        """Draws the beautiful patio, checkered green lawn, and sidewalk."""
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Background sky/hedgerow green
        surf.fill((34, 72, 38))
        
        # Top garden fence / hedge line
        pygame.draw.rect(surf, (26, 58, 30), (0, 0, SCREEN_WIDTH, GRID_START_Y))
        
        # Left house stone patio (x: 0 to GRID_START_X)
        patio_rect = (0, GRID_START_Y, GRID_START_X, self.rows * CELL_HEIGHT)
        pygame.draw.rect(surf, COLOR_PATIO, patio_rect)
        # Stone brick pattern on patio
        for r in range(self.rows * 2):
            py = GRID_START_Y + r * (CELL_HEIGHT // 2)
            pygame.draw.line(surf, COLOR_PATIO_DARK, (0, py), (GRID_START_X, py), 2)
            offset = 25 if r % 2 == 1 else 0
            for px in range(offset, GRID_START_X, 50):
                pygame.draw.line(surf, COLOR_PATIO_DARK, (px, py), (px, py + CELL_HEIGHT // 2), 2)

        # Right sidewalk / curb (x: GRID_START_X + 8 * CELL_WIDTH to SCREEN_WIDTH)
        sidewalk_x = GRID_START_X + self.cols * CELL_WIDTH
        sidewalk_rect = (sidewalk_x, GRID_START_Y, SCREEN_WIDTH - sidewalk_x, self.rows * CELL_HEIGHT)
        pygame.draw.rect(surf, COLOR_SIDEWALK, sidewalk_rect)
        for r in range(self.rows):
            sy = GRID_START_Y + r * CELL_HEIGHT
            pygame.draw.line(surf, (120, 115, 110), (sidewalk_x, sy), (SCREEN_WIDTH, sy), 2)

        # Checkered 5x8 Lawn Grid
        for r in range(self.rows):
            for c in range(self.cols):
                cx = GRID_START_X + c * CELL_WIDTH
                cy = GRID_START_Y + r * CELL_HEIGHT
                cell_color = COLOR_GRASS_LIGHT if (r + c) % 2 == 0 else COLOR_GRASS_DARK
                pygame.draw.rect(surf, cell_color, (cx, cy, CELL_WIDTH, CELL_HEIGHT))
                # Subtle grid border for clean visual clarity
                pygame.draw.rect(surf, (0, 0, 0, 20), (cx, cy, CELL_WIDTH, CELL_HEIGHT), 1)

        return surf

    def get_cell_at(self, mx, my):
        """Maps screen mouse coordinates to (row, col) or None if outside grid."""
        if not (GRID_START_X <= mx < GRID_START_X + self.cols * CELL_WIDTH):
            return None
        if not (GRID_START_Y <= my < GRID_START_Y + self.rows * CELL_HEIGHT):
            return None
        col = (mx - GRID_START_X) // CELL_WIDTH
        row = (my - GRID_START_Y) // CELL_HEIGHT
        return int(row), int(col)

    def can_plant(self, row, col):
        """Strict rule: exactly 1 plant per grid cell!"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col] is None
        return False

    def plant(self, row, col, ptype, sound_mgr, particles, diff_cfg):
        """Plants a new plant into the specified grid cell."""
        if not self.can_plant(row, col):
            return None
            
        new_plant = None
        if ptype == PLANT_SUNFLOWER:
            new_plant = Sunflower(row, col)
        elif ptype == PLANT_PEASHOOTER:
            new_plant = Peashooter(row, col)
        elif ptype == PLANT_WALLNUT:
            new_plant = Wallnut(row, col)
        elif ptype == PLANT_POTATOMINE:
            new_plant = PotatoMine(row, col, arm_multiplier=diff_cfg.get("potatomine_arm_mult", 1.0))

        if new_plant:
            self.grid[row][col] = new_plant
            sound_mgr.play("plant")
            # Planting dirt dust particles
            cx = new_plant.x + CELL_WIDTH // 2
            cy = new_plant.y + CELL_HEIGHT - 15
            for _ in range(4):
                particles.append(Particle(cx, cy, ptype="smoke"))
        return new_plant

    def remove_plant(self, row, col, sound_mgr, particles):
        """Removes a plant from the board (shovel tool)."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            p = self.grid[row][col]
            if p:
                self.grid[row][col] = None
                sound_mgr.play("plant")
                cx = p.x + CELL_WIDTH // 2
                cy = p.y + CELL_HEIGHT // 2
                for _ in range(4):
                    particles.append(Particle(cx, cy, ptype="smoke"))
                return True
        return False

    def get_plants_in_row(self, row):
        if 0 <= row < self.rows:
            return [p for p in self.grid[row] if p is not None and p.alive]
        return []

    def get_all_plants(self):
        plants = []
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.grid[r][c]
                if p is not None and p.alive:
                    plants.append(p)
        return plants

    def update(self, dt, zombies, projectiles, sun_list, sound_mgr, particles, diff_cfg):
        # Update each plant and remove dead ones
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.grid[r][c]
                if p is not None:
                    if p.alive:
                        p.update(dt, zombies, projectiles, sun_list, sound_mgr, particles, diff_cfg)
                    else:
                        self.grid[r][c] = None

        # Update lawnmowers
        for mower in self.lawnmowers:
            mower.update(dt, zombies, sound_mgr, particles)

    def check_lawnmowers(self, zombies, sound_mgr):
        """Triggers lawnmowers when a zombie approaches the house patio."""
        for z in zombies:
            if z.alive and z.x <= ZOMBIE_ALARM_X:
                mower = self.lawnmowers[z.row]
                if mower.state == "ready":
                    mower.trigger(sound_mgr)

    def check_game_over(self, zombies):
        """Returns True if any zombie breaches the house when the lawnmower is already spent."""
        for z in zombies:
            if z.alive and z.x <= ZOMBIE_LOSE_X:
                mower = self.lawnmowers[z.row]
                if mower.state == "done":
                    return True
        return False

    def draw(self, surf):
        # 1. Base lawn background
        surf.blit(self.lawn_surface, (0, 0))
        
        # 2. Lawnmowers
        for mower in self.lawnmowers:
            mower.draw(surf)

        # 3. Active plants (drawn in row order for correct depth)
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.grid[r][c]
                if p is not None and p.alive:
                    p.draw(surf)

    def draw_preview(self, surf, mx, my, selected_ptype, shovel_active=False):
        """
        Draws the plant preview following the mouse cursor.
        Highlights the hover cell in Green (valid empty cell) or Red (occupied/invalid).
        """
        cell = self.get_cell_at(mx, my)
        
        # 1. Highlight cell under mouse if hovering on grid
        if cell is not None:
            r, c = cell
            cx = GRID_START_X + c * CELL_WIDTH
            cy = GRID_START_Y + r * CELL_HEIGHT
            highlight = pygame.Surface((CELL_WIDTH, CELL_HEIGHT), pygame.SRCALPHA)
            
            if shovel_active:
                # Shovel highlights cell with plant in red/orange
                if self.grid[r][c] is not None:
                    highlight.fill((255, 60, 60, 90))
                    pygame.draw.rect(highlight, (255, 30, 30, 220), (0, 0, CELL_WIDTH, CELL_HEIGHT), 3)
                else:
                    highlight.fill((255, 255, 255, 40))
            else:
                # Plant placement: Green if empty, Red if occupied!
                if self.can_plant(r, c):
                    highlight.fill((60, 220, 80, 80)) # Green valid
                    pygame.draw.rect(highlight, (40, 255, 60, 220), (0, 0, CELL_WIDTH, CELL_HEIGHT), 3)
                else:
                    highlight.fill((220, 40, 40, 90)) # Red invalid
                    pygame.draw.rect(highlight, (255, 30, 30, 220), (0, 0, CELL_WIDTH, CELL_HEIGHT), 3)
            surf.blit(highlight, (cx, cy))

        # 2. Render plant sprite directly following cursor (semi-transparent)
        if selected_ptype is not None:
            preview_surf = None
            if selected_ptype == PLANT_SUNFLOWER:
                preview_surf = SpriteCache.get().get_sunflower(wobble_time=0.0).copy()
            elif selected_ptype == PLANT_PEASHOOTER:
                preview_surf = SpriteCache.get().get_peashooter(recoil_factor=0.0).copy()
            elif selected_ptype == PLANT_WALLNUT:
                preview_surf = SpriteCache.get().get_wallnut(damage_stage=0).copy()
            elif selected_ptype == PLANT_POTATOMINE:
                preview_surf = SpriteCache.get().get_potato_mine(armed=True, blink_on=True).copy()

            if preview_surf:
                preview_surf.set_alpha(180)
                px = mx - preview_surf.get_width() // 2
                py = my - preview_surf.get_height() // 2
                surf.blit(preview_surf, (px, py))

        # 3. Shovel cursor if shovel is active
        elif shovel_active:
            sh_sprite = SpriteCache.get().get_shovel()
            surf.blit(sh_sprite, (mx - 15, my - 35))
