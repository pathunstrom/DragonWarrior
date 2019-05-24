import random
import sys
from os import pardir
from os.path import join

import pygame
from pygame import init, Surface, QUIT
from pygame.display import set_mode, set_caption, flip
from pygame.image import load_extended
from pygame.time import Clock
from pygame.time import get_ticks
from pygame.transform import scale

import src.maps
import src.player
from src.animated_sprite import AnimatedSprite
from src.common import TILE_SIZE, SCALE


class Game(object):
    NES_RES = (256, 240)
    FPS = 60
    GAME_TITLE = "Dragon Warrior"
    WIN_WIDTH = NES_RES[0] * SCALE
    WIN_HEIGHT = NES_RES[1] * SCALE
    DATA_DIR = join(pardir, 'data')
    MUSIC_DIR = join(DATA_DIR, 'music')
    SFX_DIR = join(DATA_DIR, 'sfx')
    MAP_TILES_PATH = join(DATA_DIR, 'tileset.png')
    UNARMED_HERO_PATH = join(DATA_DIR, 'unarmed_hero.png')
    KING_LORIK_PATH = join(DATA_DIR, 'king_lorik.png')
    RIGHT_GUARD_PATH = join(DATA_DIR, 'right_guard.png')
    LEFT_GUARD_PATH = join(DATA_DIR, 'left_guard.png')
    ROAMING_GUARD_PATH = join(DATA_DIR, 'roaming_guard.png')
    COLOR_KEY = (0, 128, 128)
    ORIGIN = (0, 0)
    corner_point = [0, 0]
    BLACK = (0, 0, 0)
    BACK_FILL_COLOR = BLACK

    def __init__(self):
        # Initialize pygame
        init()

        # Create the game window.
        self.screen = set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        set_caption(self.GAME_TITLE)
        self.clock = Clock()
        self.last_roaming_character_clock_check = get_ticks()
        self.roaming_character_go_cooldown = 3000
        self.sprite_movement_wait_period = 10
        # if src.maps.current_map is None:
        #    src.maps.current_map = src.maps.TantegelThroneRoom
        #    self.player = None
        self.map_tiles = []
        self.map_tilesheet = None
        self.unarmed_hero_sheet = None
        self.king_lorik_sheet = None
        self.left_guard_sheet = None
        self.right_guard_sheet = None
        self.roaming_guard_sheet = None
        self.unarmed_hero_images = None
        self.king_lorik_images = None
        self.left_guard_images = None
        self.right_guard_images = None
        self.roaming_guard_images = None
        self.big_map_width = None
        self.big_map_height = None
        self.big_map = None
        self.current_map = None
        self.background = None
        self.load_images()

    def move_roaming_character(self):
        # TODO: extend roaming characters beyond just the roaming guard.
        for roaming_character in self.current_map.roaming_characters:
            roaming_character_direction = random.randrange(4)
            if roaming_character_direction == 0:
                now = get_ticks()
                if now - self.last_roaming_character_clock_check >= self.roaming_character_go_cooldown:
                    self.last_roaming_character_clock_check = now
                    roaming_character.direction = AnimatedSprite.DOWN
                    roaming_character.rect.y += 48
            elif roaming_character_direction == 1:
                now = get_ticks()
                if now - self.last_roaming_character_clock_check >= self.roaming_character_go_cooldown:
                    self.last_roaming_character_clock_check = now
                    roaming_character.direction = AnimatedSprite.LEFT
                    roaming_character.rect.x -= 48
            elif roaming_character_direction == 2:
                now = get_ticks()
                if now - self.last_roaming_character_clock_check >= self.roaming_character_go_cooldown:
                    self.last_roaming_character_clock_check = now
                    roaming_character.direction = AnimatedSprite.UP
                    roaming_character.rect.y -= 48
            elif roaming_character_direction == 3:
                now = get_ticks()
                if now - self.last_roaming_character_clock_check >= self.roaming_character_go_cooldown:
                    self.last_roaming_character_clock_check = now
                    roaming_character.direction = AnimatedSprite.RIGHT
                    roaming_character.rect.x += 48
            # roaming character sides collision
            if roaming_character.rect.x < 0:  # Simple Sides Collision
                roaming_character.rect.x = 0  # Reset Player Rect Coord
                # pos_x = camera_pos[0]  # Reset Camera Pos Coord
            elif roaming_character.rect.x > int(self.WIN_WIDTH - ((self.WIN_WIDTH // 24) * 1.5)):
                roaming_character.rect.x = int(self.WIN_WIDTH - ((self.WIN_WIDTH // 24) * 1.5))
                # pos_x = camera_pos[0]
            if roaming_character.rect.y < 0:
                roaming_character.rect.y = 0
                # pos_y = camera_pos[1]
            elif self.current_map.roaming_guard.rect.y > self.WIN_HEIGHT - 48:
                self.current_map.roaming_guard.rect.y = self.WIN_HEIGHT - 48

    def make_big_map(self):
        self.big_map_width = self.current_map.width
        self.big_map_height = self.current_map.height
        self.big_map = Surface((self.big_map_width, self.big_map_height)).convert()
        self.big_map.fill(self.BACK_FILL_COLOR)

    def load_current_map(self, current_map):
        if current_map == src.maps.TantegelThroneRoom:
            self.current_map = src.maps.TantegelThroneRoom(self.map_tiles, self.unarmed_hero_images,
                                                           self.king_lorik_images, self.left_guard_images,
                                                           self.right_guard_images, self.roaming_guard_images)
        elif current_map == src.maps.TantegelCourtyard:
            self.current_map = src.maps.TantegelCourtyard(self.map_tiles, self.unarmed_hero_images,
                                                          self.left_guard_images,
                                                          self.right_guard_images, self.roaming_guard_images)
        elif current_map == src.maps.Overworld:
            self.current_map = src.maps.Overworld(self.map_tiles, self.unarmed_hero_images)
        self.current_map.load_map()

    def load_images(self):
        """Load all the images for the game graphics.
        """
        # Load the map tile spritesheet
        self.map_tilesheet = load_extended(self.MAP_TILES_PATH).convert()
        # Load unarmed hero images
        self.unarmed_hero_sheet = load_extended(self.UNARMED_HERO_PATH)
        # Load King Lorik images
        self.king_lorik_sheet = load_extended(self.KING_LORIK_PATH)
        # Guard images.
        self.left_guard_sheet = load_extended(self.LEFT_GUARD_PATH)
        self.right_guard_sheet = load_extended(self.RIGHT_GUARD_PATH)
        self.roaming_guard_sheet = load_extended(self.ROAMING_GUARD_PATH)

        self.map_tilesheet = scale(self.map_tilesheet,
                                   (self.map_tilesheet.get_width() * SCALE,
                                    self.map_tilesheet.get_height() * SCALE))
        self.unarmed_hero_sheet = scale(self.unarmed_hero_sheet,
                                        (self.unarmed_hero_sheet.get_width() *
                                         SCALE,
                                         self.unarmed_hero_sheet.get_height() *
                                         SCALE))
        self.king_lorik_sheet = scale(self.king_lorik_sheet,
                                      (self.king_lorik_sheet.get_width() * SCALE,
                                       self.king_lorik_sheet.get_height() * SCALE))

        self.left_guard_sheet = scale(self.left_guard_sheet,
                                      (self.left_guard_sheet.get_width() * SCALE,
                                       self.left_guard_sheet.get_height() * SCALE))

        self.right_guard_sheet = scale(self.right_guard_sheet,
                                       (self.right_guard_sheet.get_width() * SCALE,
                                        self.right_guard_sheet.get_height() * SCALE))

        self.roaming_guard_sheet = scale(self.roaming_guard_sheet,
                                         (self.roaming_guard_sheet.get_width() * SCALE,
                                          self.roaming_guard_sheet.get_height() * SCALE))

        self.parse_map_tiles()

        # Get the images for the initial hero sprites
        self.unarmed_hero_images = self.parse_animated_spritesheet(
            self.unarmed_hero_sheet, is_roaming=True)

        # Get images for the King
        self.king_lorik_images = self.parse_animated_spritesheet(
            self.king_lorik_sheet, is_roaming=False)

        self.left_guard_images = self.parse_animated_spritesheet(
            self.left_guard_sheet, is_roaming=False)

        self.right_guard_images = self.parse_animated_spritesheet(
            self.right_guard_sheet, is_roaming=False)

        self.roaming_guard_images = self.parse_animated_spritesheet(
            self.roaming_guard_sheet, is_roaming=True)

    def parse_map_tiles(self):

        width, height = self.map_tilesheet.get_size()

        for x in range(0, width // TILE_SIZE):
            row = []
            self.map_tiles.append(row)

            for y in range(0, height // TILE_SIZE):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                row.append(self.map_tilesheet.subsurface(rect))

    def parse_animated_spritesheet(self, sheet, is_roaming=True):
        """
        Parses spritesheets and creates image lists. If is_roaming is True
        the sprite will have four lists of images, one for each direction. If
        is_roaming is False then there will be one list of 2 images.
        """
        sheet.set_colorkey(self.COLOR_KEY)
        sheet.convert_alpha()
        # width, height = sheet.get_size()

        facing_down = []
        facing_left = []
        facing_up = []
        facing_right = []

        for i in range(0, 2):

            rect = (i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
            facing_down.append(sheet.subsurface(rect))

            if is_roaming:
                rect = ((i + 2) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
                facing_left.append(sheet.subsurface(rect))

                rect = ((i + 4) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
                facing_up.append(sheet.subsurface(rect))

                rect = ((i + 6) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
                facing_right.append(sheet.subsurface(rect))

        return facing_down, facing_left, facing_up, facing_right

    def main(self):
        # This can be changed to a different map for debugging purposes.
        self.load_current_map(src.maps.Overworld)
        player = self.current_map.player
        camera_pos = (0, 0)

        # Move to map class
        # self.init_groups()
        # self.current_map = tantegel_throne_room
        # self.load_map()

        # Make the big scrollable map
        self.make_big_map()

        # self.current_map.draw_map(self.big_map)
        # self.current_map.draw_sprites(self.big_map)

        self.background = Surface(self.screen.get_size()).convert()
        self.background.fill(self.BACK_FILL_COLOR)
        # TODO: Handle maps that don't have roaming characters better.
        if self.current_map.roaming_characters:
            self.assign_roaming_guard_images()
        src.player.Player.get_hero_start_location(self.current_map.player, self.current_map)
        while True:
            self.current_map.draw_map(self.big_map)
            self.current_map.clear_sprites(self.screen, self.background)
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            camera_pos = player.move(camera_pos, self.current_map)
            # TODO: disable moving if a dialog box is open.
            # print(self.current_map.player.move(camera_pos, self.current_map))
            self.move_roaming_character()
            self.background = self.big_map.subsurface(self.corner_point[0], self.corner_point[1], self.WIN_WIDTH,
                                                      self.WIN_HEIGHT).convert()
            self.current_map.animate()
            self.current_map.draw_sprites(self.background)
            self.screen.blit(self.background, self.ORIGIN)
            self.screen.scroll(dx=camera_pos[0], dy=camera_pos[1])
            self.big_map = Surface((self.big_map_width, self.big_map_height)).convert()
            self.big_map.fill(self.BACK_FILL_COLOR)
            # self.screen.blit(self.background, self.ORIGIN)
            flip()

    def assign_roaming_guard_images(self):
        self.current_map.roaming_guard.down_images = self.roaming_guard_images[0]
        self.current_map.roaming_guard.left_images = self.roaming_guard_images[1]
        self.current_map.roaming_guard.up_images = self.roaming_guard_images[2]
        self.current_map.roaming_guard.right_images = self.roaming_guard_images[3]


if __name__ == "__main__":
    game = Game()
    game.main()
