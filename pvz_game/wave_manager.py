"""
Plantas vs Zombies - Progressive Wave Manager
Generates progressive randomized zombie waves with increasing difficulty and horde events.
"""

import random
from constants import (
    GRID_ROWS, ZOMBIE_REGULAR, ZOMBIE_CONEHEAD, ZOMBIE_BUCKETHEAD, ZOMBIE_RUNNER
)
from entities import Zombie

class WaveManager:
    def __init__(self, diff_cfg):
        self.diff_cfg = diff_cfg
        self.current_wave = 1
        self.max_wave = 10 # Endless or victory at wave 10
        
        # State machine for wave flow:
        # "pre_wave": banner countdown before first spawn
        # "spawning": zombies spawning according to queue
        # "fighting": all spawned, waiting for player to eliminate remaining zombies
        # "wave_cleared": brief victory pause before next wave
        # "victory": all waves beaten
        self.state = "pre_wave"
        self.state_timer = 3.0
        
        # Spawn queue: list of (spawn_time_offset, row, ztype)
        self.spawn_queue = []
        self.wave_elapsed = 0.0
        self.total_zombies_in_wave = 0
        self.spawned_count = 0
        self.killed_count = 0
        
        # Announcement banner
        self.banner_text = "PREPÁRATE..."
        self.banner_subtext = "Los zombis se acercan"
        self.banner_timer = 3.0
        self.is_huge_wave = False
        
        self._prepare_wave(self.current_wave)

    def set_difficulty(self, diff_cfg):
        self.diff_cfg = diff_cfg

    def _prepare_wave(self, wave_num):
        self.current_wave = wave_num
        self.wave_elapsed = 0.0
        self.spawned_count = 0
        self.killed_count = 0
        self.spawn_queue.clear()
        
        scale = self.diff_cfg.get("wave_scale_mult", 1.0)
        
        # Huge Wave occurs every 4 waves (Wave 4, Wave 8, etc.)
        self.is_huge_wave = (wave_num % 4 == 0)
        
        # Base threat budget scales progressively
        # Wave 1: budget ~ 40 (approx 2-3 regular zombies)
        # Wave 2: budget ~ 75 (approx 4-5 zombies with conehead)
        # Wave 3: budget ~ 120
        # Wave 4 (Huge Wave): budget ~ 220 (horde rush!)
        base_budget = int((30 + wave_num * 28 + (wave_num ** 1.6) * 12) * scale)
        if self.is_huge_wave:
            base_budget = int(base_budget * 1.45)
            self.banner_text = "¡SE ACERCA UNA GRAN HORDA!"
            self.banner_subtext = "¡Defiende tu jardín con todo!"
            self.banner_timer = 4.0
        else:
            self.banner_text = f"OLEADA {wave_num}"
            self.banner_subtext = "Los zombis están atacando"
            self.banner_timer = 3.0
            
        self.state = "pre_wave"
        self.state_timer = 3.5

        # Available zombie types based on wave progress
        allowed_types = [ZOMBIE_REGULAR]
        weights = [100]
        
        if wave_num >= 2:
            allowed_types.append(ZOMBIE_CONEHEAD)
            weights.append(35 + min(30, wave_num * 5))
            
        if wave_num >= 3:
            allowed_types.append(ZOMBIE_RUNNER)
            weights.append(20 + min(25, wave_num * 4))
            
        if wave_num >= 4:
            allowed_types.append(ZOMBIE_BUCKETHEAD)
            weights.append(25 + min(40, wave_num * 6))

        # Costs per zombie type:
        cost_map = {
            ZOMBIE_REGULAR: 15,
            ZOMBIE_CONEHEAD: 35,
            ZOMBIE_RUNNER: 30,
            ZOMBIE_BUCKETHEAD: 60
        }
        
        # Generate zombie list from budget
        zombie_list = []
        current_budget = base_budget
        while current_budget > 0:
            zt = random.choices(allowed_types, weights=weights)[0]
            cost = cost_map[zt]
            zombie_list.append(zt)
            current_budget -= cost
            if current_budget < min(cost_map[t] for t in allowed_types) and current_budget > 0:
                zombie_list.append(ZOMBIE_REGULAR)
                break

        self.total_zombies_in_wave = len(zombie_list)
        
        # Schedule spawn times with varied timing
        # If huge wave, a group of zombies spawns clustered at the beginning of the rush!
        current_time = 1.5
        for idx, zt in enumerate(zombie_list):
            row = random.randint(0, GRID_ROWS - 1)
            self.spawn_queue.append((current_time, row, zt))
            
            if self.is_huge_wave and idx > (len(zombie_list) // 3):
                # Faster dense rush
                gap = random.uniform(0.7, 1.8)
            else:
                # Progressive interval
                gap = random.uniform(2.0, 4.8) / scale
            current_time += gap

    def on_zombie_killed(self):
        self.killed_count += 1

    def get_wave_progress(self):
        """Returns float 0.0 to 1.0 for the HUD wave progress bar."""
        if self.total_zombies_in_wave == 0:
            return 0.0
        return min(1.0, self.killed_count / self.total_zombies_in_wave)

    def update(self, dt, zombies, sound_mgr):
        if self.banner_timer > 0:
            self.banner_timer -= dt

        if self.state == "pre_wave":
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "spawning"
                if self.is_huge_wave:
                    sound_mgr.play("zombies_coming")

        elif self.state == "spawning":
            self.wave_elapsed += dt
            
            # Spawn any queued zombies whose time has arrived
            while self.spawn_queue and self.spawn_queue[0][0] <= self.wave_elapsed:
                _, row, ztype = self.spawn_queue.pop(0)
                sp_mult = self.diff_cfg.get("zombie_speed_mult", 1.0)
                hp_mult = self.diff_cfg.get("zombie_hp_mult", 1.0)
                new_z = Zombie(row=row, ztype=ztype, speed_mult=sp_mult, hp_mult=hp_mult)
                zombies.append(new_z)
                self.spawned_count += 1
                
            if not self.spawn_queue:
                self.state = "fighting"

        elif self.state == "fighting":
            # Check if all zombies from this wave have been vanquished
            alive_count = sum(1 for z in zombies if z.alive)
            if alive_count == 0:
                self.state = "wave_cleared"
                self.state_timer = 4.0
                self.banner_text = f"¡OLEADA {self.current_wave} SUPERADA!"
                self.banner_subtext = "Buen trabajo, descansa un momento..."
                self.banner_timer = 4.0
                sound_mgr.play("game_end")

        elif self.state == "wave_cleared":
            self.state_timer -= dt
            if self.state_timer <= 0:
                if self.current_wave >= self.max_wave:
                    self.state = "victory"
                    self.banner_text = "¡VICTORIA TOTAL!"
                    self.banner_subtext = "¡Has defendido tu jardín de todas las oleadas!"
                    self.banner_timer = 999.0
                else:
                    self._prepare_wave(self.current_wave + 1)
