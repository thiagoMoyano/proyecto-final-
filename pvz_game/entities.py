"""
Plantas vs Zombies - Game Entities
Defines Plants, Zombies, Projectiles, Sun, Lawnmowers, and Visual Particles.
"""

import math
import random
import pygame
from constants import (
    CELL_WIDTH, CELL_HEIGHT, GRID_START_X, GRID_START_Y,
    PLANT_SUNFLOWER, PLANT_PEASHOOTER, PLANT_WALLNUT, PLANT_POTATOMINE, PLANT_DATA,
    ZOMBIE_REGULAR, ZOMBIE_CONEHEAD, ZOMBIE_BUCKETHEAD, ZOMBIE_RUNNER, ZOMBIE_DATA,
    LAWNMOWER_X, ZOMBIE_ALARM_X, ZOMBIE_SPAWN_X, SCREEN_WIDTH
)
from sprites import SpriteCache

# -------------------------------------------------------------
# PARTICLES & EFFECTS
# -------------------------------------------------------------
class Particle:
    def __init__(self, x, y, ptype="splat", text=None, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.ptype = ptype
        self.text = text
        self.color = color
        self.alive = True
        self.timer = 0.0
        
        if ptype == "splat":
            # Pea impact droplets
            self.max_time = 0.35
            self.droplets = []
            for _ in range(6):
                ang = random.uniform(0, 2 * math.pi)
                spd = random.uniform(40, 110)
                r = random.uniform(2, 5)
                self.droplets.append([0, 0, math.cos(ang) * spd, math.sin(ang) * spd, r])
                
        elif ptype == "spudow":
            # Big comic explosion text + flash
            self.max_time = 0.9
            self.scale = 0.4
            
        elif ptype == "smoke":
            # Explosion smoke puff
            self.max_time = 0.6
            self.radius = random.uniform(16, 28)
            self.vx = random.uniform(-30, 30)
            self.vy = random.uniform(-40, -10)
            
        elif ptype == "text":
            # Floating text like "+50"
            self.max_time = 0.8
            self.vy = -45.0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.max_time:
            self.alive = False
            return
            
        if self.ptype == "splat":
            for d in self.droplets:
                d[0] += d[2] * dt
                d[1] += d[3] * dt + 120 * dt * dt # gravity
        elif self.ptype == "spudow":
            progress = self.timer / self.max_time
            if progress < 0.2:
                self.scale = 0.4 + (progress / 0.2) * 0.9 # pop up
            else:
                self.scale = 1.3 - (progress - 0.2) * 0.3
        elif self.ptype == "smoke":
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.radius += 18 * dt
        elif self.ptype == "text":
            self.y += self.vy * dt

    def draw(self, surf, font):
        if not self.alive:
            return
            
        alpha_factor = max(0.0, 1.0 - (self.timer / self.max_time))
        alpha = int(alpha_factor * 255)
        
        if self.ptype == "splat":
            for d in self.droplets:
                dx = int(self.x + d[0])
                dy = int(self.y + d[1])
                dr = max(1, int(d[4] * alpha_factor))
                dsurf = pygame.Surface((dr * 2, dr * 2), pygame.SRCALPHA)
                pygame.draw.circle(dsurf, (110, 220, 50, alpha), (dr, dr), dr)
                surf.blit(dsurf, (dx - dr, dy - dr))
                
        elif self.ptype == "spudow":
            # Explosive starburst
            cx, cy = int(self.x), int(self.y)
            blast_r = int(48 * self.scale)
            blast_surf = pygame.Surface((blast_r * 2 + 30, blast_r * 2 + 30), pygame.SRCALPHA)
            bcx, bcy = blast_surf.get_width() // 2, blast_surf.get_height() // 2
            
            # Starburst polygon
            points = []
            n_points = 14
            for i in range(n_points):
                ang = i * (2 * math.pi / n_points)
                r = blast_r if i % 2 == 0 else blast_r * 0.55
                points.append((bcx + math.cos(ang) * r, bcy + math.sin(ang) * r))
            pygame.draw.polygon(blast_surf, (255, 60, 20, min(240, alpha)), points)
            pygame.draw.polygon(blast_surf, (255, 220, 40, min(240, alpha)), [(bcx + (p[0] - bcx) * 0.75, bcy + (p[1] - bcy) * 0.75) for p in points])
            surf.blit(blast_surf, (cx - bcx, cy - bcy))
            
            # Comic "¡SPUDOW!" text
            text_str = "¡SPUDOW!"
            t_surf = font.render(text_str, True, (255, 255, 255))
            shadow_surf = font.render(text_str, True, (40, 10, 0))
            # Scale text
            tw = max(1, int(t_surf.get_width() * self.scale))
            th = max(1, int(t_surf.get_height() * self.scale))
            scaled_t = pygame.transform.smoothscale(t_surf, (tw, th))
            scaled_sh = pygame.transform.smoothscale(shadow_surf, (tw, th))
            scaled_t.set_alpha(alpha)
            scaled_sh.set_alpha(alpha)
            surf.blit(scaled_sh, (cx - tw // 2 + 2, cy - th // 2 + 2))
            surf.blit(scaled_t, (cx - tw // 2, cy - th // 2))
            
        elif self.ptype == "smoke":
            r = int(self.radius)
            sm_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(sm_surf, (160, 160, 160, int(alpha * 0.4)), (r, r), r)
            surf.blit(sm_surf, (int(self.x) - r, int(self.y) - r))
            
        elif self.ptype == "text":
            t_surf = font.render(self.text, True, self.color)
            sh_surf = font.render(self.text, True, (0, 0, 0))
            t_surf.set_alpha(alpha)
            sh_surf.set_alpha(alpha)
            surf.blit(sh_surf, (int(self.x) + 1, int(self.y) + 1))
            surf.blit(t_surf, (int(self.x), int(self.y)))


# -------------------------------------------------------------
# PROJECTILE (PEA)
# -------------------------------------------------------------
class Projectile:
    def __init__(self, row, x, y, damage=20):
        self.row = row
        self.x = x
        self.y = y
        self.speed = 340.0
        self.damage = damage
        self.alive = True

    def update(self, dt, zombies, sound_mgr, particles):
        self.x += self.speed * dt
        if self.x > SCREEN_WIDTH + 20:
            self.alive = False
            return

        # Check collision with zombies in same row
        for z in zombies:
            if z.alive and z.row == self.row:
                # Zombie hitbox detection
                if abs(z.x + 30 - self.x) < 22:
                    z.take_damage(self.damage, sound_mgr)
                    sound_mgr.play("splat")
                    particles.append(Particle(self.x, self.y, ptype="splat"))
                    self.alive = False
                    break

    def draw(self, surf):
        pea_sprite = SpriteCache.get().get_pea()
        surf.blit(pea_sprite, (int(self.x - pea_sprite.get_width() // 2), int(self.y - pea_sprite.get_height() // 2)))


# -------------------------------------------------------------
# SUN ENTITY
# -------------------------------------------------------------
class Sun:
    def __init__(self, x, y, target_y=None, from_sky=True, value=50):
        self.x = float(x)
        self.y = float(y)
        self.target_y = float(target_y if target_y is not None else y)
        self.from_sky = from_sky
        self.value = value
        self.alive = True
        self.collected = False
        self.fly_timer = 0.0
        
        self.lifetime = 12.0 # seconds before despawn
        self.angle = 0.0
        self.pulse_phase = random.uniform(0, 6.28)
        
        # Sunflower sun arc parameters
        if not from_sky:
            self.vx = random.uniform(-25, 25)
            self.vy = -120.0
            self.gravity = 240.0
        else:
            self.fall_speed = 75.0

    def get_rect(self):
        return pygame.Rect(int(self.x - 30), int(self.y - 30), 60, 60)

    def collect(self, hud_x, hud_y):
        if not self.collected and self.alive:
            self.collected = True
            self.start_x = self.x
            self.start_y = self.y
            self.hud_x = hud_x
            self.hud_y = hud_y
            self.fly_duration = 0.45
            self.fly_timer = 0.0

    def update(self, dt, hud_x, hud_y):
        self.angle += 1.5 * dt
        self.pulse_phase += 3.0 * dt

        if self.collected:
            self.fly_timer += dt
            t = min(1.0, self.fly_timer / self.fly_duration)
            # Smooth ease-in curve toward HUD
            ease = t * t * (3.0 - 2.0 * t)
            self.x = self.start_x + (self.hud_x - self.start_x) * ease
            self.y = self.start_y + (self.hud_y - self.start_y) * ease
            if t >= 1.0:
                self.alive = False
            return True # actively collected

        # Normal falling / hopping update
        if self.from_sky:
            if self.y < self.target_y:
                self.y += self.fall_speed * dt
            else:
                self.lifetime -= dt
                if self.lifetime <= 0:
                    self.alive = False
        else:
            # Sunflower hopping arc
            if self.vy != 0 or self.y < self.target_y:
                self.x += self.vx * dt
                self.y += self.vy * dt
                self.vy += self.gravity * dt
                if self.y >= self.target_y:
                    self.y = self.target_y
                    self.vy = 0
                    self.vx = 0
            else:
                self.lifetime -= dt
                if self.lifetime <= 0:
                    self.alive = False
        return False

    def draw(self, surf):
        pulse = 1.0 + 0.08 * math.sin(self.pulse_phase)
        # Blink when nearing despawn
        if self.lifetime < 3.0 and not self.collected:
            if int(self.lifetime * 8) % 2 == 0:
                return
        sun_surf = SpriteCache.get().get_sun(angle=self.angle, pulse=pulse)
        surf.blit(sun_surf, (int(self.x - sun_surf.get_width() // 2), int(self.y - sun_surf.get_height() // 2)))


# -------------------------------------------------------------
# LAWNMOWER ENTITY
# -------------------------------------------------------------
class Lawnmower:
    def __init__(self, row):
        self.row = row
        self.x = float(LAWNMOWER_X)
        self.y = float(GRID_START_Y + row * CELL_HEIGHT + 35)
        self.state = "ready" # "ready", "active", "done"
        self.speed = 460.0
        self.reel_angle = 0.0

    def trigger(self, sound_mgr):
        if self.state == "ready":
            self.state = "active"
            sound_mgr.play("lawnmower")

    def update(self, dt, zombies, sound_mgr, particles):
        if self.state != "active":
            return
            
        self.x += self.speed * dt
        self.reel_angle += 25.0 * dt
        
        # Mow down all zombies in row touching this lawnmower
        for z in zombies:
            if z.alive and z.row == self.row:
                if z.x < self.x + 45:
                    z.die(sound_mgr, particles)
                    particles.append(Particle(z.x + 30, z.y + 40, ptype="splat"))
                    
        if self.x > SCREEN_WIDTH + 80:
            self.state = "done"

    def draw(self, surf):
        if self.state == "done":
            return
        mower_surf = SpriteCache.get().get_lawnmower(active=(self.state == "active"), reel_angle=self.reel_angle)
        surf.blit(mower_surf, (int(self.x), int(self.y)))


# -------------------------------------------------------------
# BASE PLANT CLASS
# -------------------------------------------------------------
class Plant:
    def __init__(self, row, col, ptype):
        self.row = row
        self.col = col
        self.ptype = ptype
        self.x = GRID_START_X + col * CELL_WIDTH + 5
        self.y = GRID_START_Y + row * CELL_HEIGHT + 5
        
        data = PLANT_DATA[ptype]
        self.name = data["name"]
        self.hp = data["hp"]
        self.max_hp = data["hp"]
        self.alive = True
        self.anim_timer = random.uniform(0, 5.0)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def update(self, dt, zombies, projectiles, sun_list, sound_mgr, particles, diff_cfg):
        self.anim_timer += dt

    def draw(self, surf):
        pass


class Sunflower(Plant):
    def __init__(self, row, col):
        super().__init__(row, col, PLANT_SUNFLOWER)
        # Produces sun every 18-22 seconds
        self.sun_timer = random.uniform(5.0, 9.0) # initial fast sun
        self.sun_interval = 20.0

    def update(self, dt, zombies, projectiles, sun_list, sound_mgr, particles, diff_cfg):
        super().update(dt, zombies, projectiles, sun_list, sound_mgr, particles, diff_cfg)
        self.sun_timer += dt
        if self.sun_timer >= self.sun_interval:
            self.sun_timer = 0.0
            # Spawn a sun popping out of sunflower!
            sun_val = diff_cfg["sun_value"]
            spawn_x = self.x + 42
            spawn_y = self.y + 20
            target_y = self.y + 60
            sun_list.append(Sun(spawn_x, spawn_y, target_y=target_y, from_sky=False, value=sun_val))
            particles.append(Particle(spawn_x, spawn_y - 20, ptype="text", text=f"+{sun_val}", color=(255, 235, 50)))

    def draw(self, surf):
        sf_sprite = SpriteCache.get().get_sunflower(wobble_time=self.anim_timer)
        surf.blit(sf_sprite, (self.x, self.y))


class Peashooter(Plant):
    def __init__(self, row, col):
        super().__init__(row, col, PLANT_PEASHOOTER)
        data = PLANT_DATA[PLANT_PEASHOOTER]
        self.shoot_interval = data["shoot_interval"]
        self.bullet_damage = data["bullet_damage"]
        self.shoot_timer = random.uniform(0.5, 1.0)
        self.recoil_factor = 0.0

    def update(self, dt, zombies, projectiles, sun_list, sound_mgr, particles, diff_cfg):
        super().update(dt, zombies, projectiles, sun_list, sound_mgr, particles, diff_cfg)
        
        # Decay recoil
        if self.recoil_factor > 0:
            self.recoil_factor = max(0.0, self.recoil_factor - 5.0 * dt)
            
        self.shoot_timer += dt
        
        # Check if there is any alive zombie in this row ahead of peashooter
        zombie_in_row = any(z.alive and z.row == self.row and z.x >= self.x for z in zombies)
        
        if zombie_in_row and self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            self.recoil_factor = 1.0
            sound_mgr.play("pea")
            # Launch pea projectile
            barrel_x = self.x + 64
            barrel_y = self.y + 36
            projectiles.append(Projectile(self.row, barrel_x, barrel_y, damage=self.bullet_damage))

    def draw(self, surf):
        ps_sprite = SpriteCache.get().get_peashooter(recoil_factor=self.recoil_factor)
        surf.blit(ps_sprite, (self.x, self.y))


class Wallnut(Plant):
    def __init__(self, row, col):
        super().__init__(row, col, PLANT_WALLNUT)

    def draw(self, surf):
        # Health damage stages: 0 = healthy (>66%), 1 = damaged (33-66%), 2 = heavy cracked (<33%)
        ratio = self.hp / self.max_hp
        stage = 0 if ratio > 0.66 else (1 if ratio > 0.33 else 2)
        wn_sprite = SpriteCache.get().get_wallnut(damage_stage=stage)
        surf.blit(wn_sprite, (self.x, self.y))


class PotatoMine(Plant):
    def __init__(self, row, col, arm_multiplier=1.0):
        super().__init__(row, col, PLANT_POTATOMINE)
        data = PLANT_DATA[PLANT_POTATOMINE]
        self.arm_time = data["arm_time"] * arm_multiplier
        self.explosion_damage = data["explosion_damage"]
        self.arm_timer = 0.0
        self.armed = False
        self.blink_timer = 0.0
        self.blink_state = True

    def update(self, dt, zombies, projectiles, sun_list, sound_mgr, particles, diff_cfg):
        super().update(dt, zombies, projectiles, sun_list, sound_mgr, particles, diff_cfg)
        
        if not self.armed:
            self.arm_timer += dt
            # Blink faster as it approaches full arming
            blink_interval = 0.4 - 0.25 * (self.arm_timer / self.arm_time)
            self.blink_timer += dt
            if self.blink_timer >= blink_interval:
                self.blink_timer = 0.0
                self.blink_state = not self.blink_state
                
            if self.arm_timer >= self.arm_time:
                self.armed = True
                self.blink_state = True
                sound_mgr.play("plant")
        else:
            # Check contact with zombies in cell
            cell_center_x = self.x + CELL_WIDTH // 2
            for z in zombies:
                if z.alive and z.row == self.row:
                    if abs((z.x + 30) - cell_center_x) < 32:
                        self.detonate(zombies, sound_mgr, particles)
                        break

    def detonate(self, zombies, sound_mgr, particles):
        self.alive = False
        sound_mgr.play("explosion")
        cx = self.x + CELL_WIDTH // 2
        cy = self.y + CELL_HEIGHT // 2
        
        # Explosion effects
        particles.append(Particle(cx, cy, ptype="spudow"))
        for _ in range(5):
            particles.append(Particle(cx + random.uniform(-25, 25), cy + random.uniform(-15, 15), ptype="smoke"))
            
        # Heavy damage to zombies in this cell and adjacent radius
        for z in zombies:
            if z.alive and z.row == self.row:
                if abs((z.x + 30) - cx) < 65:
                    z.take_damage(self.explosion_damage, sound_mgr)

    def draw(self, surf):
        pm_sprite = SpriteCache.get().get_potato_mine(armed=self.armed, blink_on=self.blink_state)
        surf.blit(pm_sprite, (self.x, self.y))


# -------------------------------------------------------------
# ZOMBIE BASE & SUBCLASSES
# -------------------------------------------------------------
class Zombie:
    def __init__(self, row, ztype=ZOMBIE_REGULAR, speed_mult=1.0, hp_mult=1.0):
        self.row = row
        self.ztype = ztype
        self.x = float(ZOMBIE_SPAWN_X + random.uniform(0, 50))
        self.y = float(GRID_START_Y + row * CELL_HEIGHT - 12)
        
        data = ZOMBIE_DATA[ztype]
        self.name = data["name"]
        self.base_hp = int(data["base_hp"] * hp_mult)
        self.max_base_hp = self.base_hp
        self.armor_hp = int(data["armor_hp"] * hp_mult)
        self.max_armor_hp = self.armor_hp
        self.speed = data["speed"] * speed_mult
        self.bite_dps = data["bite_dps"]
        
        self.alive = True
        self.eating = False
        self.target_plant = None
        self.walk_frame = random.uniform(0, 10.0)
        self.hit_flash_timer = 0.0
        self.chomp_sound_timer = 0.0
        self.groan_sound_timer = random.uniform(5.0, 15.0)

    @property
    def total_hp(self):
        return self.base_hp + self.armor_hp

    @property
    def max_total_hp(self):
        return self.max_base_hp + self.max_armor_hp

    def take_damage(self, amount, sound_mgr):
        self.hit_flash_timer = 0.08
        if self.armor_hp > 0:
            if amount <= self.armor_hp:
                self.armor_hp -= amount
            else:
                remaining = amount - self.armor_hp
                self.armor_hp = 0
                self.base_hp -= remaining
        else:
            self.base_hp -= amount

        if self.base_hp <= 0:
            self.base_hp = 0
            self.alive = False

    def die(self, sound_mgr, particles):
        self.alive = False
        sound_mgr.play("splat")

    def update(self, dt, board, sound_mgr, particles):
        if not self.alive:
            return
            
        if self.hit_flash_timer > 0:
            self.hit_flash_timer = max(0.0, self.hit_flash_timer - dt)
            
        # Periodic zombie groan sound
        self.groan_sound_timer -= dt
        if self.groan_sound_timer <= 0:
            self.groan_sound_timer = random.uniform(14.0, 24.0)
            sound_mgr.play("groan")

        # Check plant collision on the same row
        # Front of zombie is around self.x + 10
        front_x = self.x + 15
        plant_to_eat = None
        
        # Query board plants in this row
        for p in board.get_plants_in_row(self.row):
            if p.alive:
                plant_left = p.x
                plant_right = p.x + CELL_WIDTH - 15
                if plant_left <= front_x <= plant_right + 20:
                    plant_to_eat = p
                    break

        if plant_to_eat:
            self.eating = True
            self.target_plant = plant_to_eat
            # Bite plant
            plant_to_eat.take_damage(self.bite_dps * dt)
            self.chomp_sound_timer += dt
            if self.chomp_sound_timer >= 0.65:
                self.chomp_sound_timer = 0.0
                sound_mgr.play("chomp")
                particles.append(Particle(front_x - 5, self.y + 45, ptype="splat"))
        else:
            self.eating = False
            self.target_plant = None
            self.x -= self.speed * dt
            self.walk_frame += 1.8 * dt

    def draw(self, surf):
        if not self.alive:
            return
            
        armor_damage_ratio = 0.0
        if self.max_armor_hp > 0:
            armor_damage_ratio = 1.0 - (self.armor_hp / self.max_armor_hp)
            
        # If armor depleted on cone/buckethead, draw as regular zombie
        drawn_type = self.ztype
        if (self.ztype in (ZOMBIE_CONEHEAD, ZOMBIE_BUCKETHEAD)) and self.armor_hp <= 0:
            drawn_type = ZOMBIE_REGULAR

        z_sprite = SpriteCache.get().get_zombie(ztype=drawn_type, walk_frame=self.walk_frame, damage_ratio=armor_damage_ratio)
        
        # White flash when taking damage
        if self.hit_flash_timer > 0:
            flash_surf = z_sprite.copy()
            flash_surf.fill((255, 255, 255, 140), special_flags=pygame.BLEND_RGBA_ADD)
            surf.blit(flash_surf, (int(self.x), int(self.y)))
        else:
            surf.blit(z_sprite, (int(self.x), int(self.y)))
            
        # Draw small health bar if damaged
        if self.total_hp < self.max_total_hp and self.total_hp > 0:
            bar_w = 40
            bar_h = 5
            bx = int(self.x + 30)
            by = int(self.y - 2)
            pygame.draw.rect(surf, (40, 40, 40), (bx - 1, by - 1, bar_w + 2, bar_h + 2), border_radius=2)
            fill_w = int(bar_w * (self.total_hp / self.max_total_hp))
            bar_col = (100, 220, 50) if self.armor_hp == 0 else (240, 160, 30)
            pygame.draw.rect(surf, bar_col, (bx, by, fill_w, bar_h), border_radius=2)
