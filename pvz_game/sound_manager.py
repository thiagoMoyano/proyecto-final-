"""
Plantas vs Zombies - Sound Manager
Manages sound effects, ambient tracks, volume sliders, and mute state.
"""

import os
import pygame

class SoundManager:
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sounds_dir = os.path.join(base_dir, "assets", "sounds")
        
        # Volume settings (0.0 to 1.0)
        self.master_volume = 0.8
        self.sfx_volume = 0.85
        self.music_volume = 0.65
        self.muted = False
        
        # Audio library
        self.sounds = {}
        self.music_channel = None
        self.music_sound = None
        self.is_music_playing = False
        
        # Initialize mixer if not already done
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except Exception as e:
                print(f"[SoundManager] Warning: failed to init mixer: {e}")
                
        # Reserve channel 0 for music
        try:
            pygame.mixer.set_num_channels(16)
            self.music_channel = pygame.mixer.Channel(0)
        except Exception:
            pass
            
        self.load_all_sounds()

    def load_all_sounds(self):
        """Loads all wav sound effects from the assets/sounds directory."""
        if not os.path.exists(self.sounds_dir):
            print(f"[SoundManager] Warning: sounds directory not found: {self.sounds_dir}")
            return
            
        sound_files = {
            "pea": "pea.wav",
            "splat": "splat.wav",
            "plant": "plant.wav",
            "sun": "sun.wav",
            "chomp": "chomp.wav",
            "groan": "groan.wav",
            "explosion": "explosion.wav",
            "lawnmower": "lawnmower.wav",
            "zombies_coming": "zombies_coming.wav",
            "atebrains": "atebrains.wav",
            "game_end": "game_end.wav",
            "click": "click.wav",
            "music": "music.wav",
            "grasswalk": "grasswalk.wav"
        }
        
        for key, fname in sound_files.items():
            path = os.path.join(self.sounds_dir, fname)
            if os.path.exists(path):
                try:
                    snd = pygame.mixer.Sound(path)
                    self.sounds[key] = snd
                except Exception as e:
                    print(f"[SoundManager] Failed to load sound '{fname}': {e}")

    def effective_sfx_volume(self):
        if self.muted:
            return 0.0
        return max(0.0, min(1.0, self.master_volume * self.sfx_volume))

    def effective_music_volume(self):
        if self.muted:
            return 0.0
        return max(0.0, min(1.0, self.master_volume * self.music_volume))

    def play(self, sound_name, loops=0):
        """Plays a sound effect with current effective sfx volume."""
        if sound_name not in self.sounds:
            return None
        vol = self.effective_sfx_volume()
        if vol <= 0.0:
            return None
            
        try:
            snd = self.sounds[sound_name]
            snd.set_volume(vol)
            # Find an available channel other than channel 0 (music)
            channel = pygame.mixer.find_channel()
            if channel and channel != self.music_channel:
                channel.play(snd, loops=loops)
                return channel
            else:
                return snd.play(loops=loops)
        except Exception as e:
            return None

    def play_music(self):
        """Starts looping the background theme music."""
        music_key = "music"
        if music_key not in self.sounds:
            return
            
        self.music_sound = self.sounds[music_key]
        vol = self.effective_music_volume()
        if self.music_channel:
            self.music_channel.set_volume(vol)
            if not self.music_channel.get_busy():
                self.music_channel.play(self.music_sound, loops=-1)
        self.is_music_playing = True

    def stop_music(self):
        if self.music_channel:
            self.music_channel.stop()
        self.is_music_playing = False

    def update_volumes(self):
        """Applies updated volumes to active music and sounds."""
        if self.music_channel:
            self.music_channel.set_volume(self.effective_music_volume())

    def set_master_volume(self, val):
        self.master_volume = max(0.0, min(1.0, val))
        self.update_volumes()

    def set_sfx_volume(self, val):
        self.sfx_volume = max(0.0, min(1.0, val))
        self.update_volumes()

    def set_music_volume(self, val):
        self.music_volume = max(0.0, min(1.0, val))
        self.update_volumes()

    def toggle_mute(self):
        self.muted = not self.muted
        self.update_volumes()
        return self.muted
