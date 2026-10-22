"""
Plantas vs Zombies - UI Components & Menus
Seed packets, sun counters, wave progress, settings modal, audio sliders, and overlays.
"""

import math
import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GOLD, COLOR_WHITE, COLOR_BLACK,
    PLANT_SUNFLOWER, PLANT_PEASHOOTER, PLANT_WALLNUT, PLANT_POTATOMINE, PLANT_DATA,
    DIFFICULTY_EASY, DIFFICULTY_NORMAL, DIFFICULTY_HARD, DIFFICULTY_CONFIGS
)
from sprites import SpriteCache

class SeedPacket:
    def __init__(self, ptype, x, y, width=82, height=72):
        self.ptype = ptype
        self.rect = pygame.Rect(x, y, width, height)
        data = PLANT_DATA[ptype]
        self.name = data["name"]
        self.cost = data["cost"]
        self.max_cooldown = data["cooldown"]
        self.cooldown = 0.0 # Ready initially

    def trigger_cooldown(self):
        self.cooldown = self.max_cooldown

    def update(self, dt):
        if self.cooldown > 0:
            self.cooldown = max(0.0, self.cooldown - dt)

    def is_ready(self, current_sun):
        return self.cooldown <= 0.0 and current_sun >= self.cost

    def draw(self, surf, current_sun, font_cost, font_name):
        ready = self.is_ready(current_sun)
        
        # 1. Packet background card
        bg_col = (205, 185, 145) if ready else (150, 140, 125)
        pygame.draw.rect(surf, bg_col, self.rect, border_radius=6)
        border_col = (100, 75, 40) if ready else (80, 70, 60)
        pygame.draw.rect(surf, border_col, self.rect, 2, border_radius=6)
        
        # 2. Plant icon miniature
        icon_surf = None
        if self.ptype == PLANT_SUNFLOWER:
            icon_surf = SpriteCache.get().get_sunflower(0.0)
        elif self.ptype == PLANT_PEASHOOTER:
            icon_surf = SpriteCache.get().get_peashooter(0.0)
        elif self.ptype == PLANT_WALLNUT:
            icon_surf = SpriteCache.get().get_wallnut(0)
        elif self.ptype == PLANT_POTATOMINE:
            icon_surf = SpriteCache.get().get_potato_mine(armed=True, blink_on=True)
            
        if icon_surf:
            # Scale down to fit neatly in upper packet area
            scaled = pygame.transform.smoothscale(icon_surf, (44, 46))
            surf.blit(scaled, (self.rect.x + (self.rect.width - 44) // 2, self.rect.y + 4))

        # 3. Cost pill at bottom right
        pill_rect = pygame.Rect(self.rect.x + 2, self.rect.bottom - 20, self.rect.width - 4, 18)
        pill_col = (245, 235, 195) if ready else (175, 165, 150)
        pygame.draw.rect(surf, pill_col, pill_rect, border_radius=4)
        
        # Mini sun icon
        mini_sun = SpriteCache.get().get_sun()
        scaled_sun = pygame.transform.smoothscale(mini_sun, (16, 16))
        surf.blit(scaled_sun, (pill_rect.x + 2, pill_rect.y + 1))
        
        # Cost text
        cost_color = (0, 0, 0) if current_sun >= self.cost else (200, 30, 30)
        txt = font_cost.render(str(self.cost), True, cost_color)
        surf.blit(txt, (pill_rect.right - txt.get_width() - 4, pill_rect.y + 2))

        # 4. Cooldown overlay shade (wipes down as cooldown recharges)
        if self.cooldown > 0:
            ratio = self.cooldown / self.max_cooldown
            overlay_h = int(self.rect.height * ratio)
            if overlay_h > 0:
                shade_surf = pygame.Surface((self.rect.width, overlay_h), pygame.SRCALPHA)
                shade_surf.fill((0, 0, 0, 160))
                surf.blit(shade_surf, (self.rect.x, self.rect.y))
                # Cooldown timer text
                sec_text = font_cost.render(f"{self.cooldown:.1f}", True, (255, 255, 255))
                surf.blit(sec_text, (self.rect.centerx - sec_text.get_width() // 2, self.rect.centery - 8))
        elif current_sun < self.cost:
            # Grayed out because of insufficient sun
            shade_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            shade_surf.fill((0, 0, 0, 100))
            surf.blit(shade_surf, (self.rect.x, self.rect.y))


class Slider:
    def __init__(self, x, y, width, label, value=0.8):
        self.rect = pygame.Rect(x, y, width, 18)
        self.label = label
        self.value = value
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_val(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_val(event.pos[0])
            return True
        return False

    def _update_val(self, mx):
        rel = (mx - self.rect.x) / self.rect.width
        self.value = max(0.0, min(1.0, rel))

    def draw(self, surf, font):
        # Label
        lbl_surf = font.render(f"{self.label}: {int(self.value * 100)}%", True, (255, 255, 255))
        surf.blit(lbl_surf, (self.rect.x, self.rect.y - 20))
        
        # Track
        pygame.draw.rect(surf, (40, 40, 50), self.rect, border_radius=8)
        fill_w = int(self.rect.width * self.value)
        pygame.draw.rect(surf, (80, 190, 60), (self.rect.x, self.rect.y, fill_w, self.rect.height), border_radius=8)
        pygame.draw.rect(surf, (160, 170, 180), self.rect, 2, border_radius=8)
        
        # Handle knob
        hx = self.rect.x + fill_w
        hy = self.rect.centery
        pygame.draw.circle(surf, (240, 240, 245), (hx, hy), 12)
        pygame.draw.circle(surf, (60, 60, 70), (hx, hy), 12, 2)


class SettingsModal:
    """Settings menu for audio volumes and wave difficulty."""
    def __init__(self, sound_mgr, current_diff=DIFFICULTY_NORMAL):
        self.sound_mgr = sound_mgr
        self.current_diff = current_diff
        self.visible = False
        
        self.w = 520
        self.h = 490
        self.x = (SCREEN_WIDTH - self.w) // 2
        self.y = (SCREEN_HEIGHT - self.h) // 2
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        
        # Sliders
        sl_x = self.x + 50
        sl_w = self.w - 100
        self.slider_master = Slider(sl_x, self.y + 110, sl_w, "Volumen General", sound_mgr.master_volume)
        self.slider_sfx = Slider(sl_x, self.y + 165, sl_w, "Volumen Efectos (SFX)", sound_mgr.sfx_volume)
        self.slider_music = Slider(sl_x, self.y + 220, sl_w, "Volumen Música", sound_mgr.music_volume)
        
        # Mute button
        self.btn_mute = pygame.Rect(sl_x, self.y + 265, sl_w, 34)
        
        # Difficulty buttons (Easy, Normal, Hard)
        diff_w = (sl_w - 20) // 3
        self.btn_easy = pygame.Rect(sl_x, self.y + 345, diff_w, 36)
        self.btn_normal = pygame.Rect(sl_x + diff_w + 10, self.y + 345, diff_w, 36)
        self.btn_hard = pygame.Rect(sl_x + (diff_w + 10) * 2, self.y + 345, diff_w, 36)
        
        # Close / Resume & Restart buttons
        btn_action_w = (sl_w - 15) // 2
        self.btn_resume = pygame.Rect(sl_x, self.y + 415, btn_action_w, 42)
        self.btn_restart = pygame.Rect(sl_x + btn_action_w + 15, self.y + 415, btn_action_w, 42)

    def handle_event(self, event):
        if not self.visible:
            return None
            
        # Update sliders
        if self.slider_master.handle_event(event):
            self.sound_mgr.set_master_volume(self.slider_master.value)
        if self.slider_sfx.handle_event(event):
            self.sound_mgr.set_sfx_volume(self.slider_sfx.value)
        if self.slider_music.handle_event(event):
            self.sound_mgr.set_music_volume(self.slider_music.value)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # Mute toggle
            if self.btn_mute.collidepoint(mx, my):
                self.sound_mgr.toggle_mute()
                self.sound_mgr.play("click")
                return "mute_toggled"
                
            # Difficulty select
            if self.btn_easy.collidepoint(mx, my):
                self.current_diff = DIFFICULTY_EASY
                self.sound_mgr.play("click")
                return ("change_diff", DIFFICULTY_EASY)
            elif self.btn_normal.collidepoint(mx, my):
                self.current_diff = DIFFICULTY_NORMAL
                self.sound_mgr.play("click")
                return ("change_diff", DIFFICULTY_NORMAL)
            elif self.btn_hard.collidepoint(mx, my):
                self.current_diff = DIFFICULTY_HARD
                self.sound_mgr.play("click")
                return ("change_diff", DIFFICULTY_HARD)
                
            # Action buttons
            if self.btn_resume.collidepoint(mx, my):
                self.sound_mgr.play("click")
                self.visible = False
                return "resume"
            elif self.btn_restart.collidepoint(mx, my):
                self.sound_mgr.play("click")
                self.visible = False
                return "restart"

        return None

    def draw(self, surf, font_title, font_body):
        if not self.visible:
            return
            
        # Dimmed backdrop
        dim_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim_surf.fill((0, 0, 0, 160))
        surf.blit(dim_surf, (0, 0))
        
        # Modal window container
        pygame.draw.rect(surf, (45, 52, 40), self.rect, border_radius=14)
        pygame.draw.rect(surf, (190, 165, 90), self.rect, 4, border_radius=14)
        
        # Header title
        title_surf = font_title.render("AJUSTES DE JUEGO", True, (255, 230, 100))
        surf.blit(title_surf, (self.rect.centerx - title_surf.get_width() // 2, self.rect.y + 22))
        pygame.draw.line(surf, (150, 130, 70), (self.x + 30, self.y + 60), (self.x + self.w - 30, self.y + 60), 2)
        
        # Sliders
        self.slider_master.draw(surf, font_body)
        self.slider_sfx.draw(surf, font_body)
        self.slider_music.draw(surf, font_body)
        
        # Mute button
        mute_txt = "Silencio: ACTIVADO (MUTE)" if self.sound_mgr.muted else "Silencio: DESACTIVADO"
        mute_bg = (190, 50, 50) if self.sound_mgr.muted else (60, 75, 65)
        pygame.draw.rect(surf, mute_bg, self.btn_mute, border_radius=6)
        pygame.draw.rect(surf, (200, 200, 200), self.btn_mute, 2, border_radius=6)
        m_surf = font_body.render(mute_txt, True, (255, 255, 255))
        surf.blit(m_surf, (self.btn_mute.centerx - m_surf.get_width() // 2, self.btn_mute.centery - m_surf.get_height() // 2))

        # Difficulty section label
        diff_lbl = font_body.render("Dificultad de las Oleadas:", True, (255, 240, 180))
        surf.blit(diff_lbl, (self.x + 50, self.y + 318))
        
        # Draw 3 difficulty options
        diff_buttons = [
            (self.btn_easy, DIFFICULTY_EASY, "Fácil"),
            (self.btn_normal, DIFFICULTY_NORMAL, "Normal"),
            (self.btn_hard, DIFFICULTY_HARD, "Difícil")
        ]
        for btn, diff_key, label in diff_buttons:
            is_active = (self.current_diff == diff_key)
            btn_bg = (70, 160, 45) if is_active else (60, 65, 70)
            border_c = (255, 230, 80) if is_active else (120, 120, 120)
            pygame.draw.rect(surf, btn_bg, btn, border_radius=6)
            pygame.draw.rect(surf, border_c, btn, 3 if is_active else 1, border_radius=6)
            txt = font_body.render(label, True, (255, 255, 255))
            surf.blit(txt, (btn.centerx - txt.get_width() // 2, btn.centery - txt.get_height() // 2))

        # Resume & Restart buttons
        pygame.draw.rect(surf, (45, 140, 60), self.btn_resume, border_radius=8)
        pygame.draw.rect(surf, (255, 255, 255), self.btn_resume, 2, border_radius=8)
        res_txt = font_body.render("REANUDAR", True, (255, 255, 255))
        surf.blit(res_txt, (self.btn_resume.centerx - res_txt.get_width() // 2, self.btn_resume.centery - res_txt.get_height() // 2))

        pygame.draw.rect(surf, (170, 60, 50), self.btn_restart, border_radius=8)
        pygame.draw.rect(surf, (255, 255, 255), self.btn_restart, 2, border_radius=8)
        rst_txt = font_body.render("REINICIAR", True, (255, 255, 255))
        surf.blit(rst_txt, (self.btn_restart.centerx - rst_txt.get_width() // 2, self.btn_restart.centery - rst_txt.get_height() // 2))


class UIManager:
    def __init__(self, sound_mgr):
        self.sound_mgr = sound_mgr
        
        # Sun HUD counter
        self.sun_hud_rect = pygame.Rect(18, 12, 124, 76)
        self.sun_bounce_timer = 0.0
        
        # Initialize Seed Packets (Sunflower, Peashooter, Wall-nut, Potato Mine)
        self.packets = [
            SeedPacket(PLANT_SUNFLOWER, 155, 12),
            SeedPacket(PLANT_PEASHOOTER, 245, 12),
            SeedPacket(PLANT_WALLNUT, 335, 12),
            SeedPacket(PLANT_POTATOMINE, 425, 12)
        ]
        
        # Shovel tool button
        self.btn_shovel = pygame.Rect(525, 16, 56, 68)
        self.shovel_active = False
        
        # Wave Progress Bar
        self.wave_bar_rect = pygame.Rect(605, 32, 230, 24)
        
        # Settings button
        self.btn_settings = pygame.Rect(860, 20, 180, 48)
        
        # Active selection
        self.selected_plant_type = None
        
        # Settings modal dialog
        self.settings_modal = SettingsModal(sound_mgr)
        
        # Font caching
        self.fonts = {}
        self._init_fonts()

    def _init_fonts(self):
        try:
            self.fonts["title"] = pygame.font.SysFont("Verdana", 24, bold=True)
            self.fonts["banner"] = pygame.font.SysFont("Impact", 38)
            self.fonts["banner_sub"] = pygame.font.SysFont("Verdana", 18, bold=True)
            self.fonts["sun"] = pygame.font.SysFont("Arial", 22, bold=True)
            self.fonts["body"] = pygame.font.SysFont("Verdana", 14, bold=True)
            self.fonts["cost"] = pygame.font.SysFont("Arial", 13, bold=True)
            self.fonts["name"] = pygame.font.SysFont("Arial", 11)
        except Exception:
            self.fonts["title"] = pygame.font.Font(None, 30)
            self.fonts["banner"] = pygame.font.Font(None, 48)
            self.fonts["banner_sub"] = pygame.font.Font(None, 24)
            self.fonts["sun"] = pygame.font.Font(None, 26)
            self.fonts["body"] = pygame.font.Font(None, 20)
            self.fonts["cost"] = pygame.font.Font(None, 18)
            self.fonts["name"] = pygame.font.Font(None, 14)

    def trigger_sun_bounce(self):
        self.sun_bounce_timer = 0.25

    def get_sun_hud_pos(self):
        return (self.sun_hud_rect.centerx, self.sun_hud_rect.centery)

    def clear_selection(self):
        self.selected_plant_type = None
        self.shovel_active = False

    def handle_packet_planted(self, ptype):
        for packet in self.packets:
            if packet.ptype == ptype:
                packet.trigger_cooldown()
                break
        self.clear_selection()

    def handle_click(self, mx, my, current_sun):
        """Processes clicks on HUD elements. Returns action string or None."""
        # 1. Settings button
        if self.btn_settings.collidepoint(mx, my):
            self.sound_mgr.play("click")
            self.settings_modal.visible = True
            return "open_settings"

        # 2. Shovel button
        if self.btn_shovel.collidepoint(mx, my):
            self.sound_mgr.play("click")
            self.shovel_active = not self.shovel_active
            self.selected_plant_type = None
            return "shovel_toggled"

        # 3. Seed packets
        for packet in self.packets:
            if packet.rect.collidepoint(mx, my):
                if packet.is_ready(current_sun):
                    self.sound_mgr.play("click")
                    self.selected_plant_type = packet.ptype
                    self.shovel_active = False
                    return f"selected_{packet.ptype}"
                else:
                    return "not_enough_sun_or_cd"

        return None

    def update(self, dt):
        if self.sun_bounce_timer > 0:
            self.sun_bounce_timer = max(0.0, self.sun_bounce_timer - dt)
        for packet in self.packets:
            packet.update(dt)

    def draw_hud(self, surf, current_sun, wave_mgr):
        # Top HUD Bar container
        hud_bg = pygame.Rect(0, 0, SCREEN_WIDTH, 96)
        pygame.draw.rect(surf, (45, 32, 22), hud_bg)
        pygame.draw.rect(surf, (90, 65, 45), hud_bg, 3)

        # 1. Sun Counter Box
        pygame.draw.rect(surf, (150, 115, 65), self.sun_hud_rect, border_radius=8)
        pygame.draw.rect(surf, (230, 200, 120), self.sun_hud_rect, 3, border_radius=8)
        
        # Rotating Sun inside box
        sun_icon = SpriteCache.get().get_sun(angle=pygame.time.get_ticks() * 0.002)
        scaled_icon = pygame.transform.smoothscale(sun_icon, (40, 40))
        surf.blit(scaled_icon, (self.sun_hud_rect.x + 8, self.sun_hud_rect.y + 18))
        
        # Sun number (with punchy bounce effect when collecting)
        bounce_scale = 1.0 + (self.sun_bounce_timer / 0.25) * 0.25 if self.sun_bounce_timer > 0 else 1.0
        sun_str = str(current_sun)
        sun_surf = self.fonts["sun"].render(sun_str, True, COLOR_GOLD)
        sh_surf = self.fonts["sun"].render(sun_str, True, COLOR_BLACK)
        if bounce_scale > 1.0:
            bw = int(sun_surf.get_width() * bounce_scale)
            bh = int(sun_surf.get_height() * bounce_scale)
            sun_surf = pygame.transform.smoothscale(sun_surf, (bw, bh))
            sh_surf = pygame.transform.smoothscale(sh_surf, (bw, bh))
        tx = self.sun_hud_rect.x + 58
        ty = self.sun_hud_rect.y + 24
        surf.blit(sh_surf, (tx + 2, ty + 2))
        surf.blit(sun_surf, (tx, ty))

        # 2. Seed Packets
        for packet in self.packets:
            packet.draw(surf, current_sun, self.fonts["cost"], self.fonts["name"])
            # Highlight selected packet
            if self.selected_plant_type == packet.ptype:
                pygame.draw.rect(surf, (255, 235, 50), packet.rect, 3, border_radius=6)

        # 3. Shovel Tool
        sh_bg = (140, 80, 50) if not self.shovel_active else (210, 60, 40)
        pygame.draw.rect(surf, sh_bg, self.btn_shovel, border_radius=8)
        sh_border = (255, 235, 100) if self.shovel_active else (80, 45, 25)
        pygame.draw.rect(surf, sh_border, self.btn_shovel, 3, border_radius=8)
        sh_icon = SpriteCache.get().get_shovel()
        surf.blit(sh_icon, (self.btn_shovel.x + (self.btn_shovel.width - sh_icon.get_width()) // 2, self.btn_shovel.y + 6))

        # 4. Wave Progress Bar
        bar_bg = (50, 45, 40)
        pygame.draw.rect(surf, bar_bg, self.wave_bar_rect, border_radius=6)
        prog = wave_mgr.get_wave_progress()
        fill_w = int(self.wave_bar_rect.width * prog)
        if fill_w > 0:
            fill_col = (70, 190, 50) if not wave_mgr.is_huge_wave else (230, 70, 30)
            pygame.draw.rect(surf, fill_col, (self.wave_bar_rect.x, self.wave_bar_rect.y, fill_w, self.wave_bar_rect.height), border_radius=6)
        pygame.draw.rect(surf, (200, 190, 170), self.wave_bar_rect, 2, border_radius=6)
        
        # Wave label
        wave_txt = f"Oleada {wave_mgr.current_wave}"
        w_surf = self.fonts["body"].render(wave_txt, True, (255, 255, 255))
        surf.blit(w_surf, (self.wave_bar_rect.centerx - w_surf.get_width() // 2, self.wave_bar_rect.y - 18))
        
        # Zombie head flag marker on progress bar
        marker_x = int(self.wave_bar_rect.x + self.wave_bar_rect.width - (self.wave_bar_rect.width * prog))
        pygame.draw.circle(surf, (140, 175, 130), (marker_x, self.wave_bar_rect.centery), 9)
        pygame.draw.circle(surf, (20, 20, 20), (marker_x, self.wave_bar_rect.centery), 9, 2)
        pygame.draw.circle(surf, (255, 40, 40), (marker_x - 3, self.wave_bar_rect.centery - 2), 2)

        # 5. Settings / Pause Button
        pygame.draw.rect(surf, (60, 105, 50), self.btn_settings, border_radius=8)
        pygame.draw.rect(surf, (180, 230, 140), self.btn_settings, 2, border_radius=8)
        gear_txt = self.fonts["body"].render("AJUSTES / PAUSA", True, (255, 255, 255))
        surf.blit(gear_txt, (self.btn_settings.centerx - gear_txt.get_width() // 2, self.btn_settings.centery - gear_txt.get_height() // 2))

    def draw_banner(self, surf, wave_mgr):
        """Displays wave announcement banners ('OLEADA X', '¡GRAN HORDA!')."""
        if wave_mgr.banner_timer > 0:
            alpha = min(255, int((wave_mgr.banner_timer / 0.5) * 255)) if wave_mgr.banner_timer < 0.5 else 240
            banner_surf = pygame.Surface((SCREEN_WIDTH, 110), pygame.SRCALPHA)
            banner_bg_col = (180, 25, 25, alpha) if wave_mgr.is_huge_wave else (25, 55, 30, alpha)
            banner_surf.fill(banner_bg_col)
            pygame.draw.line(banner_surf, (255, 220, 60, alpha), (0, 0), (SCREEN_WIDTH, 0), 4)
            pygame.draw.line(banner_surf, (255, 220, 60, alpha), (0, 108), (SCREEN_WIDTH, 108), 4)
            
            # Big banner title
            t_surf = self.fonts["banner"].render(wave_mgr.banner_text, True, (255, 240, 80))
            sh_surf = self.fonts["banner"].render(wave_mgr.banner_text, True, (0, 0, 0))
            cx = SCREEN_WIDTH // 2
            banner_surf.blit(sh_surf, (cx - t_surf.get_width() // 2 + 3, 15 + 3))
            banner_surf.blit(t_surf, (cx - t_surf.get_width() // 2, 15))
            
            # Subtext
            st_surf = self.fonts["banner_sub"].render(wave_mgr.banner_subtext, True, (255, 255, 255))
            banner_surf.blit(st_surf, (cx - st_surf.get_width() // 2, 68))
            
            surf.blit(banner_surf, (0, 240))
