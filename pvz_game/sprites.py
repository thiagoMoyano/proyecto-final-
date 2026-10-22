"""
Plantas vs Zombies - Procedural Sprite Generator & Cache
Renders high quality stylized cartoon sprites for plants, zombies, items, and UI.
"""

import math
import pygame
from constants import (
    PLANT_SUNFLOWER, PLANT_PEASHOOTER, PLANT_WALLNUT, PLANT_POTATOMINE,
    ZOMBIE_REGULAR, ZOMBIE_CONEHEAD, ZOMBIE_BUCKETHEAD, ZOMBIE_RUNNER
)

class SpriteCache:
    _instance = None
    
    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = SpriteCache()
        return cls._instance

    def __init__(self):
        self.cache = {}
        
    # -------------------------------------------------------------
    # HELPER DRAWING UTILITIES
    # -------------------------------------------------------------
    def _draw_ellipse(self, surf, color, rect, width=0):
        pygame.draw.ellipse(surf, color, rect, width)

    def _draw_shadow(self, surf, center_x, ground_y, radius_x=32, radius_y=12):
        """Draws a soft translucent oval ground shadow."""
        shadow_surf = pygame.Surface((radius_x * 2, radius_y * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 75), (0, 0, radius_x * 2, radius_y * 2))
        surf.blit(shadow_surf, (center_x - radius_x, ground_y - radius_y))

    # -------------------------------------------------------------
    # SUN SPRITE
    # -------------------------------------------------------------
    def get_sun(self, angle=0.0, pulse=1.0):
        """Generates a radiant golden sun with animated rotating rays."""
        size = 72
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2
        
        # Outer rays
        ray_count = 12
        ray_len = 26 * pulse
        ray_width = 7
        for i in range(ray_count):
            a = angle + (i * (2 * math.pi / ray_count))
            x1 = cx + math.cos(a) * (14 * pulse)
            y1 = cy + math.sin(a) * (14 * pulse)
            x2 = cx + math.cos(a) * (ray_len + 6)
            y2 = cy + math.sin(a) * (ray_len + 6)
            pygame.draw.line(surf, (255, 175, 20), (int(x1), int(y1)), (int(x2), int(y2)), int(ray_width))
            pygame.draw.line(surf, (255, 235, 70), (int(x1), int(y1)), (int(x2), int(y2)), int(ray_width - 2))

        # Core glowing circle
        core_r = int(18 * pulse)
        pygame.draw.circle(surf, (255, 160, 20), (cx, cy), core_r + 3)
        pygame.draw.circle(surf, (255, 225, 40), (cx, cy), core_r)
        pygame.draw.circle(surf, (255, 250, 150), (cx - 4, cy - 4), core_r // 2)
        
        # Cute kawaii face on sun
        eye_y = cy - 2
        pygame.draw.ellipse(surf, (60, 30, 0), (cx - 8, eye_y, 4, 6))
        pygame.draw.ellipse(surf, (60, 30, 0), (cx + 4, eye_y, 4, 6))
        pygame.draw.circle(surf, (255, 255, 255), (cx - 7, eye_y + 1), 1)
        pygame.draw.circle(surf, (255, 255, 255), (cx + 5, eye_y + 1), 1)
        # Happy smile
        pygame.draw.arc(surf, (80, 40, 0), (cx - 5, cy, 10, 8), math.pi, 2 * math.pi, 2)
        # Rosy cheeks
        pygame.draw.circle(surf, (255, 130, 80, 160), (cx - 10, cy + 3), 3)
        pygame.draw.circle(surf, (255, 130, 80, 160), (cx + 10, cy + 3), 3)

        return surf

    # -------------------------------------------------------------
    # PROJECTILE (PEA)
    # -------------------------------------------------------------
    def get_pea(self):
        key = "bullet_pea"
        if key in self.cache:
            return self.cache[key]
            
        size = 28
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2
        r = 11
        
        # Soft outer glow
        pygame.draw.circle(surf, (70, 180, 30, 90), (cx, cy), r + 3)
        # Base green
        pygame.draw.circle(surf, (40, 120, 20), (cx, cy), r)
        pygame.draw.circle(surf, (100, 210, 45), (cx - 1, cy - 1), r - 2)
        pygame.draw.circle(surf, (160, 245, 90), (cx - 3, cy - 3), r - 5)
        # White highlight gleam
        pygame.draw.circle(surf, (255, 255, 255), (cx - 4, cy - 4), 3)
        
        self.cache[key] = surf
        return surf

    # -------------------------------------------------------------
    # PLANTS
    # -------------------------------------------------------------
    def get_sunflower(self, wobble_time=0.0):
        """Sunflower with breathing wobble, glowing petals and cute face."""
        size_w, size_h = 90, 95
        surf = pygame.Surface((size_w, size_h), pygame.SRCALPHA)
        cx, cy = size_w // 2, 42
        
        # Wobble factor
        wobble = math.sin(wobble_time * 3.5) * 4.0
        
        # Ground shadow
        self._draw_shadow(surf, size_w // 2, 85, 28, 9)
        
        # Green Stem & Leaves
        stem_color = (65, 150, 40)
        stem_highlight = (95, 190, 60)
        # Left leaf
        pygame.draw.ellipse(surf, stem_color, (14, 64, 30, 16))
        pygame.draw.ellipse(surf, stem_highlight, (16, 65, 24, 11))
        # Right leaf
        pygame.draw.ellipse(surf, stem_color, (46, 65, 30, 16))
        pygame.draw.ellipse(surf, stem_highlight, (48, 66, 24, 11))
        # Stem curve
        stem_pts = [(cx, cy + 18), (cx + int(wobble * 0.4), 65), (cx, 84)]
        pygame.draw.lines(surf, stem_color, False, stem_pts, 8)
        pygame.draw.lines(surf, stem_highlight, False, stem_pts, 4)
        
        # Animated head center
        hx = cx + int(wobble)
        hy = cy
        
        # Petals (10 radiating petals)
        petal_count = 10
        petal_w, petal_h = 16, 26
        for i in range(petal_count):
            ang = (i * (2 * math.pi / petal_count)) + (wobble_time * 0.5)
            px = hx + math.cos(ang) * 19
            py = hy + math.sin(ang) * 19
            # Draw petal as rotated ellipse on a sub-surface
            psurf = pygame.Surface((petal_w, petal_h), pygame.SRCALPHA)
            pygame.draw.ellipse(psurf, (230, 150, 10), (0, 0, petal_w, petal_h))
            pygame.draw.ellipse(psurf, (255, 215, 30), (2, 2, petal_w - 4, petal_h - 4))
            pygame.draw.ellipse(psurf, (255, 245, 120), (4, 4, petal_w - 8, petal_h - 10))
            
            deg = math.degrees(-ang) - 90
            rotated_petal = pygame.transform.rotate(psurf, deg)
            surf.blit(rotated_petal, (px - rotated_petal.get_width() // 2, py - rotated_petal.get_height() // 2))

        # Center disc (brown rich seed bed)
        pygame.draw.circle(surf, (90, 50, 15), (hx, hy), 20)
        pygame.draw.circle(surf, (130, 75, 25), (hx, hy), 18)
        
        # Cute Smiling Face
        # Eyes
        eye_y = hy - 4
        pygame.draw.ellipse(surf, (20, 10, 5), (hx - 9, eye_y, 6, 9))
        pygame.draw.ellipse(surf, (20, 10, 5), (hx + 3, eye_y, 6, 9))
        # Eye shine
        pygame.draw.circle(surf, (255, 255, 255), (hx - 8, eye_y + 2), 2)
        pygame.draw.circle(surf, (255, 255, 255), (hx + 4, eye_y + 2), 2)
        # Happy smile
        pygame.draw.arc(surf, (40, 20, 5), (hx - 6, hy, 12, 11), math.pi, 2 * math.pi, 3)
        # Rosy Cheeks
        pygame.draw.circle(surf, (240, 110, 90, 160), (hx - 12, hy + 4), 4)
        pygame.draw.circle(surf, (240, 110, 90, 160), (hx + 12, hy + 4), 4)

        return surf

    def get_peashooter(self, recoil_factor=0.0):
        """Peashooter with snout cannon, eye, and shooting recoil."""
        size_w, size_h = 90, 95
        surf = pygame.Surface((size_w, size_h), pygame.SRCALPHA)
        cx, cy = 40, 42
        
        # Recoil displacement
        rx = -int(recoil_factor * 8.0)
        
        # Ground shadow
        self._draw_shadow(surf, 45, 85, 26, 9)
        
        # Base Leaves
        stem_col = (50, 140, 30)
        leaf_hi = (90, 195, 55)
        pygame.draw.ellipse(surf, stem_col, (15, 70, 28, 16))
        pygame.draw.ellipse(surf, leaf_hi, (18, 71, 20, 11))
        pygame.draw.ellipse(surf, stem_col, (45, 72, 28, 14))
        pygame.draw.ellipse(surf, leaf_hi, (47, 73, 20, 10))
        
        # Stem curve
        stem_pts = [(cx + rx, cy + 18), (cx + rx - 5, 65), (cx + 5, 84)]
        pygame.draw.lines(surf, stem_col, False, stem_pts, 8)
        pygame.draw.lines(surf, leaf_hi, False, stem_pts, 4)
        
        # Back leaf tendril on head
        pygame.draw.ellipse(surf, stem_col, (cx + rx - 26, cy - 8, 16, 12))
        pygame.draw.ellipse(surf, leaf_hi, (cx + rx - 24, cy - 7, 12, 8))
        
        # Head (Round sphere)
        hx = cx + rx
        hy = cy
        pygame.draw.circle(surf, (40, 130, 25), (hx, hy), 22)
        pygame.draw.circle(surf, (85, 190, 45), (hx - 1, hy - 1), 20)
        pygame.draw.circle(surf, (135, 230, 75), (hx - 5, hy - 5), 14)
        
        # Snout / Cannon tube (pointing right)
        snout_x = hx + 14
        snout_y = hy - 4
        snout_w = 26 + int(recoil_factor * 4)
        snout_h = 18
        pygame.draw.ellipse(surf, (40, 130, 25), (snout_x - 4, snout_y, snout_w, snout_h))
        pygame.draw.ellipse(surf, (85, 190, 45), (snout_x - 3, snout_y + 1, snout_w - 2, snout_h - 2))
        # Snout mouth opening (dark hole inside)
        rim_x = snout_x + snout_w - 8
        pygame.draw.ellipse(surf, (30, 80, 15), (rim_x, snout_y - 2, 12, snout_h + 4))
        pygame.draw.ellipse(surf, (15, 45, 10), (rim_x + 2, snout_y, 8, snout_h))
        
        # Eye (big cartoon eye looking forward)
        eye_x = hx + 3
        eye_y = hy - 9
        pygame.draw.ellipse(surf, (20, 20, 20), (eye_x, eye_y, 9, 13))
        pygame.draw.ellipse(surf, (255, 255, 255), (eye_x + 1, eye_y + 1, 7, 11))
        # Pupil looking right
        pygame.draw.ellipse(surf, (20, 20, 20), (eye_x + 3, eye_y + 3, 5, 7))
        pygame.draw.circle(surf, (255, 255, 255), (eye_x + 4, eye_y + 4), 2)
        
        return surf

    def get_wallnut(self, damage_stage=0):
        """Wall-nut with expressive face and health damage cracks."""
        size_w, size_h = 90, 95
        surf = pygame.Surface((size_w, size_h), pygame.SRCALPHA)
        cx, cy = size_w // 2, 48
        
        # Ground shadow
        self._draw_shadow(surf, cx, 86, 28, 10)
        
        # Nut body (oval)
        nut_w, nut_h = 52, 66
        body_rect = (cx - nut_w // 2, cy - nut_h // 2, nut_w, nut_h)
        # Shadow / outline
        pygame.draw.ellipse(surf, (100, 65, 25), body_rect)
        # Base warm brown
        pygame.draw.ellipse(surf, (170, 115, 55), (body_rect[0] + 3, body_rect[1] + 3, nut_w - 6, nut_h - 6))
        # Highlight zone
        pygame.draw.ellipse(surf, (210, 155, 80), (body_rect[0] + 6, body_rect[1] + 5, nut_w - 18, nut_h - 18))
        
        # Eyes
        eye_y = cy - 8
        # Left eye
        pygame.draw.ellipse(surf, (30, 20, 10), (cx - 16, eye_y, 11, 15))
        pygame.draw.ellipse(surf, (255, 255, 255), (cx - 15, eye_y + 1, 9, 13))
        # Right eye
        pygame.draw.ellipse(surf, (30, 20, 10), (cx + 5, eye_y, 11, 15))
        pygame.draw.ellipse(surf, (255, 255, 255), (cx + 6, eye_y + 1, 9, 13))
        
        if damage_stage == 0:
            # Happy smiling healthy walnut
            pygame.draw.circle(surf, (30, 20, 10), (cx - 11, eye_y + 7), 3)
            pygame.draw.circle(surf, (30, 20, 10), (cx + 10, eye_y + 7), 3)
            pygame.draw.arc(surf, (50, 25, 10), (cx - 8, cy + 6, 16, 10), math.pi, 2 * math.pi, 3)
            
        elif damage_stage == 1:
            # Concerned / damaged walnut with cracks
            pygame.draw.circle(surf, (30, 20, 10), (cx - 11, eye_y + 5), 3)
            pygame.draw.circle(surf, (30, 20, 10), (cx + 10, eye_y + 5), 3)
            # Worried wavy mouth
            pts = [(cx - 9, cy + 12), (cx - 3, cy + 9), (cx + 3, cy + 13), (cx + 9, cy + 10)]
            pygame.draw.lines(surf, (50, 25, 10), False, pts, 3)
            # Visible crack on right side
            crack_pts = [(cx + 16, cy - 20), (cx + 12, cy - 8), (cx + 19, cy + 2), (cx + 14, cy + 16)]
            pygame.draw.lines(surf, (70, 35, 10), False, crack_pts, 3)
            
        else:
            # Heavily damaged crying / fractured walnut
            pygame.draw.circle(surf, (30, 20, 10), (cx - 11, eye_y + 4), 3)
            pygame.draw.circle(surf, (30, 20, 10), (cx + 10, eye_y + 4), 3)
            # Tear drops
            pygame.draw.ellipse(surf, (100, 190, 255), (cx - 14, eye_y + 14, 5, 8))
            pygame.draw.ellipse(surf, (100, 190, 255), (cx + 10, eye_y + 14, 5, 8))
            # Open screaming / stressed mouth
            pygame.draw.ellipse(surf, (40, 15, 10), (cx - 9, cy + 9, 18, 14))
            pygame.draw.ellipse(surf, (220, 70, 70), (cx - 6, cy + 15, 12, 7))
            # Massive cracks and bite chunk
            crack1 = [(cx - 20, cy - 14), (cx - 12, cy - 4), (cx - 15, cy + 10), (cx - 8, cy + 22)]
            crack2 = [(cx + 14, cy - 24), (cx + 9, cy - 10), (cx + 18, cy + 4), (cx + 11, cy + 18)]
            pygame.draw.lines(surf, (50, 20, 5), False, crack1, 3)
            pygame.draw.lines(surf, (50, 20, 5), False, crack2, 3)
            # Missing chunk taken by zombies
            pygame.draw.circle(surf, (35, 75, 45, 0), (cx + 24, cy - 10), 10)

        return surf

    def get_potato_mine(self, armed=False, blink_on=True):
        """Potato Mine: subterranean mound with flashing red antenna, or popped-up armed smiling potato!"""
        size_w, size_h = 90, 95
        surf = pygame.Surface((size_w, size_h), pygame.SRCALPHA)
        cx = size_w // 2
        
        # Ground dirt mound
        mound_rect = (cx - 30, 66, 60, 22)
        pygame.draw.ellipse(surf, (70, 45, 20), mound_rect)
        pygame.draw.ellipse(surf, (105, 70, 30), (cx - 26, 68, 52, 16))
        # Small dirt scatter pebbles
        pygame.draw.circle(surf, (80, 50, 20), (cx - 24, 78), 3)
        pygame.draw.circle(surf, (80, 50, 20), (cx + 22, 77), 4)
        pygame.draw.circle(surf, (80, 50, 20), (cx + 12, 83), 3)
        
        if not armed:
            # Submerged state: only top dome and blinking red LED antenna
            pygame.draw.ellipse(surf, (140, 95, 45), (cx - 16, 56, 32, 22))
            # Antenna stalk
            pygame.draw.line(surf, (60, 60, 60), (cx, 58), (cx, 44), 3)
            # LED Light (blinks on / off)
            led_col = (255, 30, 30) if blink_on else (100, 20, 20)
            pygame.draw.circle(surf, led_col, (cx, 43), 6)
            if blink_on:
                pygame.draw.circle(surf, (255, 180, 180), (cx - 1, 41), 2)
                # Soft red halo
                halo = pygame.Surface((24, 24), pygame.SRCALPHA)
                pygame.draw.circle(halo, (255, 50, 50, 80), (12, 12), 11)
                surf.blit(halo, (cx - 12, 31))
        else:
            # Fully Armed State: pops out cheerful, ready to explode!
            py = 52
            # Potato body
            pygame.draw.ellipse(surf, (120, 80, 35), (cx - 22, py - 20, 44, 42))
            pygame.draw.ellipse(surf, (175, 125, 60), (cx - 19, py - 18, 38, 36))
            pygame.draw.ellipse(surf, (215, 160, 85), (cx - 14, py - 14, 22, 20))
            
            # Cute eyes
            pygame.draw.ellipse(surf, (20, 20, 20), (cx - 12, py - 10, 8, 11))
            pygame.draw.ellipse(surf, (255, 255, 255), (cx - 11, py - 9, 6, 9))
            pygame.draw.circle(surf, (20, 20, 20), (cx - 8, py - 4), 2)
            
            pygame.draw.ellipse(surf, (20, 20, 20), (cx + 4, py - 10, 8, 11))
            pygame.draw.ellipse(surf, (255, 255, 255), (cx + 5, py - 9, 6, 9))
            pygame.draw.circle(surf, (20, 20, 20), (cx + 8, py - 4), 2)
            
            # Antenna with bright golden yellow ready bulb
            pygame.draw.line(surf, (50, 50, 50), (cx, py - 20), (cx, py - 32), 3)
            pygame.draw.circle(surf, (255, 220, 0), (cx, py - 33), 6)
            pygame.draw.circle(surf, (255, 255, 200), (cx - 1, py - 35), 2)
            
            # Happy smiling mouth ("SPUDOW" ready)
            pygame.draw.arc(surf, (50, 30, 10), (cx - 7, py + 2, 14, 10), math.pi, 2 * math.pi, 3)

        return surf

    # -------------------------------------------------------------
    # ZOMBIES
    # -------------------------------------------------------------
    def get_zombie(self, ztype=ZOMBIE_REGULAR, walk_frame=0, damage_ratio=0.0):
        """Generates stylized PvZ zombie with animated walk sway and armor accessories."""
        size_w, size_h = 100, 115
        surf = pygame.Surface((size_w, size_h), pygame.SRCALPHA)
        
        # Ground shadow
        self._draw_shadow(surf, 48, 102, 28, 10)
        
        # Walk frame wobble
        sway = math.sin(walk_frame * 0.35) * 4.0
        leg_offset = math.sin(walk_frame * 0.35) * 8.0
        
        cx = 50 + int(sway * 0.5)
        cy = 50
        
        skin_color = (135, 172, 140)
        skin_shadow = (100, 135, 105)
        suit_brown = (110, 75, 45)
        shirt_yellow = (230, 225, 180)
        tie_red = (210, 45, 40)
        pants_blue = (70, 75, 95)
        
        # 1. Back Arm (clumsy outstretched zombie arm)
        pygame.draw.line(surf, suit_brown, (cx - 2, cy - 5), (cx - 24, cy - 2), 7)
        pygame.draw.line(surf, skin_color, (cx - 24, cy - 2), (cx - 36, cy + 4), 6)
        
        # 2. Legs
        # Left leg (back)
        pygame.draw.line(surf, pants_blue, (cx - 6, cy + 18), (cx - 12 - int(leg_offset * 0.5), cy + 48), 8)
        # Right leg (front with torn knee)
        knee_x = cx + 8 + int(leg_offset * 0.5)
        pygame.draw.line(surf, pants_blue, (cx + 6, cy + 18), (knee_x, cy + 34), 8)
        # Bare green knee
        pygame.draw.circle(surf, skin_color, (knee_x, cy + 34), 4)
        pygame.draw.line(surf, pants_blue, (knee_x, cy + 34), (knee_x + 4, cy + 48), 8)
        # Shoes
        pygame.draw.ellipse(surf, (45, 30, 20), (cx - 18 - int(leg_offset * 0.5), cy + 46, 15, 8))
        pygame.draw.ellipse(surf, (45, 30, 20), (knee_x - 2, cy + 46, 16, 8))
        
        # 3. Torso (Brown ragged suit jacket)
        torso_rect = (cx - 14, cy - 10, 26, 32)
        pygame.draw.rect(surf, suit_brown, torso_rect, border_radius=4)
        # Yellowed collared shirt center V
        pygame.draw.polygon(surf, shirt_yellow, [(cx - 4, cy - 10), (cx + 4, cy - 10), (cx, cy + 2)])
        # Red necktie hanging sideways
        tie_pts = [(cx - 2, cy - 6), (cx + 2, cy - 6), (cx + 4, cy + 10), (cx, cy + 14), (cx - 4, cy + 10)]
        pygame.draw.polygon(surf, tie_red, tie_pts)
        
        # 4. Front Arm (limp reaching out forward)
        pygame.draw.line(surf, suit_brown, (cx - 4, cy - 2), (cx - 28, cy + 6), 8)
        pygame.draw.line(surf, skin_color, (cx - 28, cy + 6), (cx - 44, cy + 12), 6)
        # Clumsy green zombie fingers
        pygame.draw.circle(surf, skin_color, (cx - 45, cy + 12), 4)
        
        # 5. Head
        hx = cx - 4
        hy = cy - 24
        # Head shape (slightly squarish top, jutting lower jaw)
        pygame.draw.circle(surf, skin_shadow, (hx, hy), 19)
        pygame.draw.circle(surf, skin_color, (hx - 1, hy - 1), 18)
        # Jutting lower jaw
        jaw_rect = (hx - 16, hy + 4, 20, 14)
        pygame.draw.ellipse(surf, skin_shadow, jaw_rect)
        pygame.draw.ellipse(surf, skin_color, (hx - 15, hy + 5, 18, 12))
        
        # Bulging cartoon zombie eyes
        # Left eye (smaller pupil)
        pygame.draw.ellipse(surf, (20, 20, 20), (hx - 16, hy - 8, 11, 14))
        pygame.draw.ellipse(surf, (255, 255, 240), (hx - 15, hy - 7, 9, 12))
        pygame.draw.circle(surf, (20, 20, 20), (hx - 11, hy - 2), 2)
        # Right eye (wide bulging)
        pygame.draw.ellipse(surf, (20, 20, 20), (hx - 4, hy - 9, 13, 16))
        pygame.draw.ellipse(surf, (255, 255, 240), (hx - 3, hy - 8, 11, 14))
        pygame.draw.circle(surf, (20, 20, 20), (hx + 1, hy - 2), 3)
        
        # Gaping mouth with yellow crooked teeth
        mouth_rect = (hx - 14, hy + 7, 14, 8)
        pygame.draw.ellipse(surf, (40, 20, 20), mouth_rect)
        # Teeth
        pygame.draw.rect(surf, (240, 230, 150), (hx - 12, hy + 7, 3, 4))
        pygame.draw.rect(surf, (240, 230, 150), (hx - 5, hy + 9, 3, 4))
        
        # 6. Armor & Accessories based on Zombie Type
        if ztype == ZOMBIE_CONEHEAD:
            cone_base_y = hy - 14
            # Orange traffic cone
            cone_w = 34
            cone_h = 36
            cone_pts = [
                (hx - cone_w // 2, cone_base_y),
                (hx + cone_w // 2 - 4, cone_base_y),
                (hx - 2, cone_base_y - cone_h)
            ]
            pygame.draw.polygon(surf, (245, 115, 15), cone_pts)
            # White reflective stripe on cone
            stripe_pts = [
                (hx - 10, cone_base_y - 12),
                (hx + 6, cone_base_y - 12),
                (hx + 3, cone_base_y - 20),
                (hx - 7, cone_base_y - 20)
            ]
            pygame.draw.polygon(surf, (245, 245, 245), stripe_pts)
            # Black base rim
            pygame.draw.ellipse(surf, (220, 95, 10), (hx - cone_w // 2 - 2, cone_base_y - 4, cone_w + 4, 8))
            # Cracks if damaged
            if damage_ratio > 0.4:
                pygame.draw.line(surf, (50, 20, 0), (hx - 4, cone_base_y - 6), (hx + 1, cone_base_y - 22), 2)
                
        elif ztype == ZOMBIE_BUCKETHEAD:
            bucket_y = hy - 20
            # Silver metallic galvanized bucket
            bucket_w = 38
            bucket_h = 30
            b_rect = (hx - bucket_w // 2, bucket_y, bucket_w, bucket_h)
            # Bucket base
            pygame.draw.rect(surf, (160, 165, 175), b_rect, border_top_left_radius=6, border_top_right_radius=6)
            # Metallic shine stripe
            pygame.draw.rect(surf, (220, 225, 235), (hx - 4, bucket_y + 2, 8, bucket_h - 4))
            # Bucket rim
            pygame.draw.ellipse(surf, (120, 125, 135), (hx - bucket_w // 2 - 2, bucket_y + bucket_h - 6, bucket_w + 4, 10))
            # Handle hanging down
            pygame.draw.arc(surf, (90, 95, 100), (hx - bucket_w // 2 - 4, bucket_y + 4, bucket_w + 8, 28), math.pi, 2 * math.pi, 3)
            # Dent if damaged
            if damage_ratio > 0.4:
                pygame.draw.ellipse(surf, (90, 95, 105), (hx + 3, bucket_y + 8, 9, 9))

        elif ztype == ZOMBIE_RUNNER:
            # Red athletic headband and striped jersey!
            headband_y = hy - 14
            pygame.draw.ellipse(surf, (220, 30, 30), (hx - 16, headband_y, 30, 8))
            # Red athletic track jacket
            pygame.draw.rect(surf, (220, 30, 30), (torso_rect[0] + 1, torso_rect[1] + 1, torso_rect[2] - 2, torso_rect[3] - 2), border_radius=4)
            # White race stripe
            pygame.draw.line(surf, (255, 255, 255), (cx - 2, cy - 8), (cx - 2, cy + 20), 3)

        return surf

    # -------------------------------------------------------------
    # LAWNMOWER
    # -------------------------------------------------------------
    def get_lawnmower(self, active=False, reel_angle=0.0):
        """Classic red lawnmower with spinning silver blades and black wheels."""
        size_w, size_h = 75, 60
        surf = pygame.Surface((size_w, size_h), pygame.SRCALPHA)
        
        # Shadow
        self._draw_shadow(surf, 35, 52, 28, 7)
        
        # Black Handle
        pygame.draw.line(surf, (40, 40, 40), (8, 12), (24, 34), 4)
        pygame.draw.circle(surf, (200, 30, 30), (8, 12), 4)
        
        # Red Engine Body Housing
        body_rect = (16, 22, 38, 22)
        pygame.draw.rect(surf, (190, 25, 25), body_rect, border_radius=5)
        pygame.draw.rect(surf, (230, 50, 50), (18, 24, 34, 10), border_radius=3)
        # Engine vents
        for vx in range(22, 48, 6):
            pygame.draw.line(surf, (80, 10, 10), (vx, 30), (vx, 38), 2)
            
        # Front Reel Cutter Cylinder (silver metal)
        reel_cx, reel_cy = 54, 38
        reel_r = 14
        pygame.draw.circle(surf, (180, 185, 195), (reel_cx, reel_cy), reel_r)
        pygame.draw.circle(surf, (120, 125, 135), (reel_cx, reel_cy), reel_r, 2)
        # Spinning spiral blade lines
        for b in range(4):
            ang = reel_angle + (b * (math.pi / 2))
            bx = reel_cx + math.cos(ang) * (reel_r - 2)
            by = reel_cy + math.sin(ang) * (reel_r - 2)
            pygame.draw.line(surf, (240, 245, 255), (reel_cx, reel_cy), (int(bx), int(by)), 2)

        # Wheels
        pygame.draw.circle(surf, (35, 35, 35), (22, 44), 9)
        pygame.draw.circle(surf, (180, 180, 180), (22, 44), 4)
        pygame.draw.circle(surf, (35, 35, 35), (46, 44), 8)
        pygame.draw.circle(surf, (180, 180, 180), (46, 44), 3)

        return surf

    # -------------------------------------------------------------
    # SHOVEL ICON
    # -------------------------------------------------------------
    def get_shovel(self):
        key = "shovel_icon"
        if key in self.cache:
            return self.cache[key]
            
        size = 56
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        # Wooden shaft
        pygame.draw.line(surf, (160, 105, 50), (12, 44), (36, 20), 6)
        # Wooden D-handle
        pygame.draw.ellipse(surf, (130, 80, 35), (8, 38, 12, 12), 3)
        # Steel Blade
        blade_pts = [(32, 24), (46, 10), (48, 16), (38, 30)]
        pygame.draw.polygon(surf, (180, 190, 200), blade_pts)
        pygame.draw.polygon(surf, (230, 235, 245), [(34, 22), (44, 12), (42, 18), (36, 26)])
        
        self.cache[key] = surf
        return surf
