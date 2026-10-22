"""
Plantas vs Zombies - Main Game Loop
Entry point for the Plants vs Zombies Pygame replica.
"""

import sys
import os
import random
# Ensure current script folder is first in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    DIFFICULTY_NORMAL, DIFFICULTY_CONFIGS,
    PLANT_DATA, GRID_START_X, GRID_START_Y, CELL_WIDTH, CELL_HEIGHT, GRID_COLS, GRID_ROWS
)
from sound_manager import SoundManager
from sprites import SpriteCache
from lawn_board import Board
from wave_manager import WaveManager
from ui import UIManager
from entities import Sun, Particle

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        
        # Display setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Audio manager
        self.sound_mgr = SoundManager()
        
        # Difficulty configuration
        self.current_diff_key = DIFFICULTY_NORMAL
        self.diff_cfg = DIFFICULTY_CONFIGS[self.current_diff_key]
        
        # Fonts
        self._init_fonts()
        
        # Game State
        self.state = "playing" # "playing", "paused", "game_over", "victory"
        self.game_over_sound_played = False
        
        # Init all game systems
        self.reset_game()
        
        # Start theme music
        self.sound_mgr.play_music()

    def _init_fonts(self):
        try:
            self.font_large = pygame.font.SysFont("Impact", 54)
            self.font_sub = pygame.font.SysFont("Verdana", 22, bold=True)
            self.font_btn = pygame.font.SysFont("Verdana", 18, bold=True)
        except Exception:
            self.font_large = pygame.font.Font(None, 64)
            self.font_sub = pygame.font.Font(None, 28)
            self.font_btn = pygame.font.Font(None, 24)

    def reset_game(self):
        self.diff_cfg = DIFFICULTY_CONFIGS[self.current_diff_key]
        self.sun = self.diff_cfg["initial_sun"]
        
        self.board = Board()
        self.wave_mgr = WaveManager(self.diff_cfg)
        self.ui_mgr = UIManager(self.sound_mgr)
        self.ui_mgr.settings_modal.current_diff = self.current_diff_key
        
        self.zombies = []
        self.projectiles = []
        self.sun_list = []
        self.particles = []
        
        # Sky Sun Spawner Timer
        min_i, max_i = self.diff_cfg["sky_sun_interval"]
        self.sky_sun_timer = random.uniform(3.0, 6.0)
        self.sky_sun_interval = random.uniform(min_i, max_i)
        
        self.state = "playing"
        self.game_over_sound_played = False

    def change_difficulty(self, new_diff_key):
        self.current_diff_key = new_diff_key
        self.diff_cfg = DIFFICULTY_CONFIGS[new_diff_key]
        self.wave_mgr.set_difficulty(self.diff_cfg)

    def spawn_sky_sun(self):
        """Spawns a sun dropping from the sky onto a random lawn column & row."""
        # Random X across the lawn columns
        col = random.randint(0, GRID_COLS - 1)
        row = random.randint(0, GRID_ROWS - 1)
        spawn_x = GRID_START_X + col * CELL_WIDTH + CELL_WIDTH // 2
        spawn_y = -30
        target_y = GRID_START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2
        val = self.diff_cfg["sun_value"]
        self.sun_list.append(Sun(spawn_x, spawn_y, target_y=target_y, from_sky=True, value=val))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Settings modal event handling
            if self.ui_mgr.settings_modal.visible:
                action = self.ui_mgr.settings_modal.handle_event(event)
                if action == "resume":
                    self.state = "playing"
                elif action == "restart":
                    self.reset_game()
                elif isinstance(action, tuple) and action[0] == "change_diff":
                    self.change_difficulty(action[1])
                continue

            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.ui_mgr.selected_plant_type or self.ui_mgr.shovel_active:
                        self.ui_mgr.clear_selection()
                    else:
                        # Toggle pause / settings
                        self.ui_mgr.settings_modal.visible = not self.ui_mgr.settings_modal.visible
                        self.sound_mgr.play("click")
                elif event.key == pygame.K_1:
                    # Hotkey plant 1
                    self.ui_mgr.handle_click(160, 20, self.sun)
                elif event.key == pygame.K_2:
                    # Hotkey plant 2
                    self.ui_mgr.handle_click(250, 20, self.sun)
                elif event.key == pygame.K_3:
                    # Hotkey plant 3
                    self.ui_mgr.handle_click(340, 20, self.sun)
                elif event.key == pygame.K_4:
                    # Hotkey plant 4
                    self.ui_mgr.handle_click(430, 20, self.sun)

            # Mouse interaction during normal play
            if self.state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    
                    # Right click: cancel active selection
                    if event.button == 3:
                        self.ui_mgr.clear_selection()
                        continue
                        
                    if event.button == 1:
                        # 1. First priority: Check clicking on falling or produced Suns!
                        clicked_sun = False
                        for s in reversed(self.sun_list):
                            if s.alive and not s.collected and s.get_rect().collidepoint(mx, my):
                                hud_x, hud_y = self.ui_mgr.get_sun_hud_pos()
                                s.collect(hud_x, hud_y)
                                self.sound_mgr.play("sun")
                                self.sun += s.value
                                self.ui_mgr.trigger_sun_bounce()
                                self.particles.append(Particle(mx, my - 15, ptype="text", text=f"+{s.value}", color=(255, 235, 60)))
                                clicked_sun = True
                                break
                        if clicked_sun:
                            continue

                        # 2. Check clicking HUD controls (seed packets, shovel, settings button)
                        if my <= 96:
                            action = self.ui_mgr.handle_click(mx, my, self.sun)
                            if action and action.startswith("selected_"):
                                self.drag_origin_packet = True
                            continue

                        # 3. Handle lawn clicking with active plant selection
                        if self.ui_mgr.selected_plant_type is not None:
                            cell = self.board.get_cell_at(mx, my)
                            if cell is not None:
                                r, c = cell
                                # Strict rule: only 1 plant per cell!
                                if self.board.can_plant(r, c):
                                    cost = PLANT_DATA[self.ui_mgr.selected_plant_type]["cost"]
                                    if self.sun >= cost:
                                        self.sun -= cost
                                        self.board.plant(r, c, self.ui_mgr.selected_plant_type, self.sound_mgr, self.particles, self.diff_cfg)
                                        self.ui_mgr.handle_packet_planted(self.ui_mgr.selected_plant_type)
                            continue

                        # 4. Handle lawn clicking with active shovel tool
                        if self.ui_mgr.shovel_active:
                            cell = self.board.get_cell_at(mx, my)
                            if cell is not None:
                                r, c = cell
                                if self.board.remove_plant(r, c, self.sound_mgr, self.particles):
                                    self.ui_mgr.clear_selection()
                            continue

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Drag-and-drop release support
                    mx, my = event.pos
                    if getattr(self, "drag_origin_packet", False) and self.ui_mgr.selected_plant_type is not None:
                        self.drag_origin_packet = False
                        if my > 96:
                            cell = self.board.get_cell_at(mx, my)
                            if cell is not None:
                                r, c = cell
                                if self.board.can_plant(r, c):
                                    cost = PLANT_DATA[self.ui_mgr.selected_plant_type]["cost"]
                                    if self.sun >= cost:
                                        self.sun -= cost
                                        self.board.plant(r, c, self.ui_mgr.selected_plant_type, self.sound_mgr, self.particles, self.diff_cfg)
                                        self.ui_mgr.handle_packet_planted(self.ui_mgr.selected_plant_type)

            # Game Over & Victory restart click handling
            elif self.state in ("game_over", "victory"):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    btn_replay = pygame.Rect((SCREEN_WIDTH - 240) // 2, 430, 240, 52)
                    if btn_replay.collidepoint(mx, my):
                        self.sound_mgr.play("click")
                        self.reset_game()

    def update(self, dt):
        # Always update UI cooldowns and particles
        self.ui_mgr.update(dt)
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]

        # Stop updates if modal settings is open
        if self.ui_mgr.settings_modal.visible:
            return

        if self.state == "playing":
            # 1. Sky Sun Spawning
            self.sky_sun_timer += dt
            if self.sky_sun_timer >= self.sky_sun_interval:
                self.sky_sun_timer = 0.0
                min_i, max_i = self.diff_cfg["sky_sun_interval"]
                self.sky_sun_interval = random.uniform(min_i, max_i)
                self.spawn_sky_sun()

            # 2. Update Suns
            hud_x, hud_y = self.ui_mgr.get_sun_hud_pos()
            for s in self.sun_list:
                s.update(dt, hud_x, hud_y)
            self.sun_list = [s for s in self.sun_list if s.alive]

            # 3. Update Board & Plants
            self.board.update(dt, self.zombies, self.projectiles, self.sun_list, self.sound_mgr, self.particles, self.diff_cfg)
            
            # 4. Update Projectiles
            for proj in self.projectiles:
                proj.update(dt, self.zombies, self.sound_mgr, self.particles)
            self.projectiles = [p for p in self.projectiles if p.alive]

            # 5. Update Zombies
            alive_before = len(self.zombies)
            for z in self.zombies:
                z.update(dt, self.board, self.sound_mgr, self.particles)
            
            # Check zombies killed this frame
            for z in self.zombies:
                if not z.alive:
                    self.wave_mgr.on_zombie_killed()
                    self.particles.append(Particle(z.x + 30, z.y + 40, ptype="splat"))
            self.zombies = [z for z in self.zombies if z.alive]

            # 6. Lawnmower activations
            self.board.check_lawnmowers(self.zombies, self.sound_mgr)

            # 7. Check Game Over condition (zombies reached the house past spent lawnmower)
            if self.board.check_game_over(self.zombies):
                self.state = "game_over"
                if not self.game_over_sound_played:
                    self.sound_mgr.play("atebrains")
                    self.game_over_sound_played = True

            # 8. Update Wave Manager
            self.wave_mgr.update(dt, self.zombies, self.sound_mgr)
            if self.wave_mgr.state == "victory":
                self.state = "victory"

    def draw(self):
        # 1. Base lawn background, lawnmowers, plants
        self.board.draw(self.screen)

        # 2. Draw Projectiles
        for proj in self.projectiles:
            proj.draw(self.screen)

        # 3. Draw Zombies (ordered by Y coordinate for correct perspective layering)
        sorted_zombies = sorted(self.zombies, key=lambda z: z.y)
        for z in sorted_zombies:
            z.draw(self.screen)

        # 4. Draw Suns
        for s in self.sun_list:
            s.draw(self.screen)

        # 5. Draw Particles
        for p in self.particles:
            p.draw(self.screen, self.font_sub)

        # 6. Draw Plant follow preview / Shovel hover
        mx, my = pygame.mouse.get_pos()
        if self.state == "playing" and not self.ui_mgr.settings_modal.visible:
            self.board.draw_preview(self.screen, mx, my, self.ui_mgr.selected_plant_type, shovel_active=self.ui_mgr.shovel_active)

        # 7. Draw HUD (sun count, seed packet cards, progress bar, shovel)
        self.ui_mgr.draw_hud(self.screen, self.sun, self.wave_mgr)

        # 8. Draw Wave announcement banner
        self.ui_mgr.draw_banner(self.screen, self.wave_mgr)

        # 9. Draw Game Over Overlay
        if self.state == "game_over":
            self._draw_game_over_screen()

        # 10. Draw Victory Overlay
        elif self.state == "victory":
            self._draw_victory_screen()

        # 11. Draw Settings / Pause Modal Dialog
        self.ui_mgr.settings_modal.draw(self.screen, self.font_large, self.font_btn)

        pygame.display.flip()

    def _draw_game_over_screen(self):
        dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((20, 0, 0, 205))
        self.screen.blit(dim, (0, 0))
        
        # Red warning banner
        text_go = "¡LOS ZOMBIES SE COMIERON TU CEREBRO!"
        t_surf = self.font_large.render(text_go, True, (255, 40, 40))
        sh_surf = self.font_large.render(text_go, True, (0, 0, 0))
        cx = SCREEN_WIDTH // 2
        self.screen.blit(sh_surf, (cx - t_surf.get_width() // 2 + 4, 230 + 4))
        self.screen.blit(t_surf, (cx - t_surf.get_width() // 2, 230))
        
        sub = self.font_sub.render(f"Llegaste hasta la Oleada {self.wave_mgr.current_wave}", True, (240, 240, 240))
        self.screen.blit(sub, (cx - sub.get_width() // 2, 320))

        # Replay Button
        btn_replay = pygame.Rect((SCREEN_WIDTH - 240) // 2, 430, 240, 52)
        pygame.draw.rect(self.screen, (190, 45, 40), btn_replay, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), btn_replay, 3, border_radius=10)
        r_txt = self.font_btn.render("VOLVER A JUGAR", True, (255, 255, 255))
        self.screen.blit(r_txt, (btn_replay.centerx - r_txt.get_width() // 2, btn_replay.centery - r_txt.get_height() // 2))

    def _draw_victory_screen(self):
        dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((10, 40, 15, 200))
        self.screen.blit(dim, (0, 0))
        
        text_vic = "¡VICTORIA! ¡JARDÍN A SALVO!"
        t_surf = self.font_large.render(text_vic, True, (255, 230, 60))
        sh_surf = self.font_large.render(text_vic, True, (0, 0, 0))
        cx = SCREEN_WIDTH // 2
        self.screen.blit(sh_surf, (cx - t_surf.get_width() // 2 + 4, 220 + 4))
        self.screen.blit(t_surf, (cx - t_surf.get_width() // 2, 220))
        
        sub = self.font_sub.render("¡Has derrotado a todas las oleadas de zombis!", True, (240, 255, 240))
        self.screen.blit(sub, (cx - sub.get_width() // 2, 310))

        # Replay Button
        btn_replay = pygame.Rect((SCREEN_WIDTH - 240) // 2, 430, 240, 52)
        pygame.draw.rect(self.screen, (40, 160, 60), btn_replay, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), btn_replay, 3, border_radius=10)
        r_txt = self.font_btn.render("JUGAR DE NUEVO", True, (255, 255, 255))
        self.screen.blit(r_txt, (btn_replay.centerx - r_txt.get_width() // 2, btn_replay.centery - r_txt.get_height() // 2))

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05) # Prevent physics glitches on window lag
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    game = Game()
    game.run()
