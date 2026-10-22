"""
Plantas vs Zombies - Constants & Configurations
"""

# Screen & Window
SCREEN_WIDTH = 1060
SCREEN_HEIGHT = 650
FPS = 60
TITLE = "Plantas vs Zombies - Python Edition"

# Colors (RGB / RGBA)
COLOR_BG = (35, 75, 45)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_TEXT_SHADOW = (20, 20, 20)
COLOR_GOLD = (255, 215, 0)
COLOR_GOLD_DARK = (218, 165, 32)
COLOR_SUN_CORE = (255, 245, 120)
COLOR_SUN_ORANGE = (255, 160, 20)

# Lawn checkered colors
COLOR_GRASS_LIGHT = (112, 195, 48)
COLOR_GRASS_DARK = (96, 172, 38)
COLOR_GRASS_GRID_LINE = (80, 150, 30, 80)
COLOR_PATIO = (128, 128, 136)
COLOR_PATIO_DARK = (108, 108, 116)
COLOR_SIDEWALK = (150, 142, 134)

# Grid Geometry (Exact 5 rows x 8 playable columns)
GRID_ROWS = 5
GRID_COLS = 8
CELL_WIDTH = 95
CELL_HEIGHT = 100
GRID_START_X = 190
GRID_START_Y = 105

# Lawnmowers & Boundaries
LAWNMOWER_X = 130
ZOMBIE_SPAWN_X = SCREEN_WIDTH + 40
ZOMBIE_ALARM_X = 180
ZOMBIE_LOSE_X = 110

# Plant Types
PLANT_SUNFLOWER = "sunflower"
PLANT_PEASHOOTER = "peashooter"
PLANT_WALLNUT = "wallnut"
PLANT_POTATOMINE = "potatomine"

# Plant Specifications
# cost: soles, cooldown: seconds, hp: health points
PLANT_DATA = {
    PLANT_SUNFLOWER: {
        "name": "Girasol",
        "cost": 50,
        "cooldown": 7.5,
        "hp": 300,
        "desc": "Genera soles para tu jardín"
    },
    PLANT_PEASHOOTER: {
        "name": "Lanzaguisantes",
        "cost": 100,
        "cooldown": 7.5,
        "hp": 300,
        "shoot_interval": 1.4,
        "bullet_damage": 20,
        "desc": "Dispara guisantes a los zombis"
    },
    PLANT_WALLNUT: {
        "name": "Nuez",
        "cost": 50,
        "cooldown": 20.0,
        "hp": 4000,
        "desc": "Gran resistencia para frenar zombis"
    },
    PLANT_POTATOMINE: {
        "name": "Papapum",
        "cost": 25,
        "cooldown": 20.0,
        "hp": 300,
        "arm_time": 10.0,
        "explosion_damage": 1800,
        "desc": "Mina que explota al contacto"
    }
}

# Zombie Types
ZOMBIE_REGULAR = "regular"
ZOMBIE_CONEHEAD = "conehead"
ZOMBIE_BUCKETHEAD = "buckethead"
ZOMBIE_RUNNER = "runner"

ZOMBIE_DATA = {
    ZOMBIE_REGULAR: {
        "name": "Zombi Común",
        "base_hp": 200,
        "armor_hp": 0,
        "speed": 22.0, # px per sec
        "bite_dps": 100.0,
        "points": 10
    },
    ZOMBIE_CONEHEAD: {
        "name": "Zombi Caracono",
        "base_hp": 200,
        "armor_hp": 360,
        "speed": 22.0,
        "bite_dps": 100.0,
        "points": 25
    },
    ZOMBIE_BUCKETHEAD: {
        "name": "Zombi Caracubo",
        "base_hp": 200,
        "armor_hp": 900,
        "speed": 22.0,
        "bite_dps": 100.0,
        "points": 45
    },
    ZOMBIE_RUNNER: {
        "name": "Zombi Atleta",
        "base_hp": 220,
        "armor_hp": 0,
        "speed": 40.0,
        "bite_dps": 100.0,
        "points": 30
    }
}

# Difficulty Settings
DIFFICULTY_EASY = "easy"
DIFFICULTY_NORMAL = "normal"
DIFFICULTY_HARD = "hard"

DIFFICULTY_CONFIGS = {
    DIFFICULTY_EASY: {
        "label": "Fácil",
        "initial_sun": 150,
        "sun_value": 50,
        "sky_sun_interval": (6.5, 9.0),
        "zombie_speed_mult": 0.82,
        "zombie_hp_mult": 0.85,
        "wave_scale_mult": 0.75,
        "potatomine_arm_mult": 0.8,
    },
    DIFFICULTY_NORMAL: {
        "label": "Normal",
        "initial_sun": 100,
        "sun_value": 50,
        "sky_sun_interval": (8.0, 11.0),
        "zombie_speed_mult": 1.0,
        "zombie_hp_mult": 1.0,
        "wave_scale_mult": 1.0,
        "potatomine_arm_mult": 1.0,
    },
    DIFFICULTY_HARD: {
        "label": "Difícil",
        "initial_sun": 50,
        "sun_value": 25,
        "sky_sun_interval": (10.0, 13.0),
        "zombie_speed_mult": 1.20,
        "zombie_hp_mult": 1.15,
        "wave_scale_mult": 1.35,
        "potatomine_arm_mult": 1.2,
    }
}
