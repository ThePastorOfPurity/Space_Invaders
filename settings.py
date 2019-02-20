from pygame import mixer

class Settings():

    def __init__(self):
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # ship
        self.ship_speed_factor = None
        self.ship_limit = 3

        # bullet
        self.bullet_speed_factor = 4
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # alien
        self.alien_speed_factor = None
        self.fleet_drop_speed = 10
        self.fleet_direction = None

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        # bunker
        self.bunker_size = 10
        self.bunker_color = (0,255,0)

        # laser
        self.laser_speed_factor = None
        self.lasers_allowed = 1
        self.laser_stamp = None
        self.laser_time = 1000

        # sound
        self.audio_channels = 5
        self.music_channel = mixer.Channel
        self.music = mixer.Sound('resources/music.wav')

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""

        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.laser_speed_factor = 1.5
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values"""

        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

