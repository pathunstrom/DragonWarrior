from os.path import join

import pygame
from pygame.sprite import Group, RenderUpdates

from src import game
from src.animated_sprite import AnimatedSprite
from src.base_sprite import BaseSprite
from src.common import TILE_SIZE
from src.player import Player

# Tile Key:
# Index values for the map tiles corresponding to location on tilesheet.
ROOF = 0
WALL = 1
WOOD = 2
BRICK = 3
CHEST = 4
DOOR = 5
BRICK_STAIR_DOWN = 6
BRICK_STAIR_UP = 7
BARRIER = 8
WEAPON_SIGN = 9
INN_SIGN = 10
CASTLE = 11
TOWN = 12
GRASS = 13
TREES = 14
HILLS = 15
MOUNTAINS = 16
CAVE = 17
GRASS_STAIR_DOWN = 18
SAND = 19
MARSH = 20
BRIDGE = 21
WATER = 22
BOTTOM_COAST = 23
BOTTOM_LEFT_COAST = 24
LEFT_COAST = 25
TOP_LEFT_COAST = 26
TOP_COAST = 27
TOP_RIGHT_COAST = 28
RIGHT_COAST = 29
BOTTOM_RIGHT_COAST = 30
BOTTOM_TOP_LEFT_COAST = 31
BOTTOM_TOP_COAST = 32
BOTTOM_TOP_RIGHT_COAST = 33
HERO = 34
KING_LORIK = 35
LEFT_GUARD = 36
RIGHT_GUARD = 37
ROAMING_GUARD = 38

impassable_objects = [ROOF, WALL, WOOD, DOOR, BARRIER, WEAPON_SIGN, INN_SIGN, MOUNTAINS, WATER, BOTTOM_COAST,
                      BOTTOM_LEFT_COAST, LEFT_COAST, TOP_LEFT_COAST, TOP_COAST, TOP_RIGHT_COAST, RIGHT_COAST,
                      BOTTOM_RIGHT_COAST, BOTTOM_TOP_LEFT_COAST, BOTTOM_TOP_COAST, BOTTOM_TOP_RIGHT_COAST, KING_LORIK,
                      LEFT_GUARD, RIGHT_GUARD]

tantegel_throne_room = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 4, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 2, 2, 2, 2, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 35, 2, 2, 3, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 34, 4, 4, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 38, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 37, 3, 36, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 3, 3, 6, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# 30 x 30
tantegel_courtyard = [
    [1, 1, 1, 1, 1, 1, 1, 13, 13, 13, 13, 13, 13, 13, 13, 1, 1, 1, 1, 1, 1, 1, 13, 1, 1, 1, 13, 14, 13, 13],
    [1, 3, 3, 3, 3, 3, 1, 13, 14, 13, 14, 14, 13, 14, 13, 1, 3, 3, 3, 3, 3, 1, 13, 1, 3, 1, 13, 13, 13, 13],
    [1, 3, 3, 3, 3, 3, 1, 13, 13, 13, 13, 13, 13, 13, 13, 1, 3, 3, 3, 3, 3, 1, 13, 1, 2, 1, 13, 13, 13, 13],
    [1, 3, 3, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 3, 3, 1, 13, 13, 13, 14, 14, 13, 13, 13],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3],
    [1, 1, 1, 1, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 1, 3, 1, 34, 3, 3, 3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 1, 3, 1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3],
    [1, 1, 1, 1, 1, 3, 1, 14, 14, 3, 3, 3, 3, 14, 14, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 1, 3, 1, 14, 14, 3, 3, 3, 3, 14, 14, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 1, 3, 1, 14, 13, 3, 3, 3, 3, 13, 14, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 4, 3, 3, 5, 3, 1, 13, 13, 3, 3, 3, 3, 13, 13, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 4, 3, 1, 3, 1, 13, 13, 3, 3, 3, 3, 13, 13, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 4, 3, 4, 1, 3, 1, 13, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 1, 1, 1, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

overworld = [
    [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 30, 13, 13, 13, 13, 13, 13, 24, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 30, 13, 13, 13, 14, 14, 14, 14, 13, 13, 24, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 29, 13, 13, 12, 14, 14, 14, 14, 14, 14, 13, 13, 24, 23, 23, 23, 23, 22, 22, 22, 22, 22, 22],
    [22, 22, 29, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 29, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 16, 16, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 29, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 29, 14, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 29, 15, 15, 15, 15, 15, 34, 16, 16, 16, 16, 16, 14, 14, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 29, 15, 15, 15, 15, 16, 16, 16, 16, 14, 14, 14, 14, 14, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 29, 15, 15, 15, 15, 16, 16, 14, 14, 14, 14, 14, 14, 14, 14, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 29, 15, 15, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 27, 28, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 22, 28, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 22, 22, 28, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
]

current_map = None


# Working on class refactoring of maps


class DragonWarriorMap(object):
    def __init__(self, map_tiles, hero_images=None):

        if hero_images is None:
            hero_images = []
        self.door_group = Group()
        self.chest_group = Group()
        self.brick_group = Group()
        self.wood_group = Group()
        self.wall_group = Group()
        self.roof_group = Group()
        self.grass_group = Group()
        self.brick_stair_down_group = Group()
        self.brick_stair_up_group = Group()
        self.barrier_group = Group()
        self.weapon_sign_group = Group()
        self.inn_sign_group = Group()
        self.castle_group = Group()
        self.town_group = Group()
        self.trees_group = Group()
        self.hills_group = Group()
        self.mountains_group = Group()
        self.cave_group = Group()
        self.grass_stair_down_group = Group()
        self.sand_group = Group()
        self.marsh_group = Group()
        self.bridge_group = Group()
        self.water_group = Group()
        self.bottom_coast_group = Group()
        self.bottom_left_coast_group = Group()
        self.left_coast_group = Group()
        self.top_left_coast_group = Group()
        self.top_coast_group = Group()
        self.top_right_coast_group = Group()
        self.right_coast_group = Group()
        self.bottom_right_coast_group = Group()
        self.bottom_top_left_coast_group = Group()
        self.bottom_top_coast_group = Group()
        self.bottom_top_right_coast_group = Group()
        self.roaming_characters = []
        self.tile_groups = [self.door_group, self.chest_group, self.brick_group, self.wood_group, self.wall_group,
                            self.roof_group, self.grass_group, self.brick_stair_down_group, self.brick_stair_up_group,
                            self.barrier_group, self.weapon_sign_group, self.inn_sign_group, self.castle_group,
                            self.town_group, self.trees_group, self.hills_group, self.mountains_group, self.cave_group,
                            self.grass_stair_down_group, self.sand_group, self.marsh_group, self.bridge_group,
                            self.water_group, self.bottom_coast_group, self.bottom_left_coast_group,
                            self.left_coast_group, self.top_left_coast_group, self.top_coast_group,
                            self.top_right_coast_group, self.right_coast_group, self.bottom_right_coast_group,
                            self.bottom_top_left_coast_group, self.bottom_top_coast_group,
                            self.bottom_top_right_coast_group]
        self.map_tiles = map_tiles
        self.hero_images = hero_images
        self.center_pt = None
        self.player = None
        self.player_sprites = None
        self.npc_sprites = []
        self.layout = None
        self.npcs = []
        self.bgm = ""

    def load_map(self):
        current_loaded_map = self

        x_offset = TILE_SIZE / 2
        y_offset = TILE_SIZE / 2

        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                self.center_pt = [(x * TILE_SIZE) + x_offset,
                                  (y * TILE_SIZE) + y_offset]
                if self.layout[y][x] == ROOF:
                    roof = BaseSprite(self.center_pt, self.map_tiles[ROOF][0])
                    self.roof_group.add(roof)
                elif self.layout[y][x] == WALL:
                    wall = BaseSprite(self.center_pt, self.map_tiles[WALL][0])
                    self.wall_group.add(wall)
                elif self.layout[y][x] == WOOD:
                    wood = BaseSprite(self.center_pt, self.map_tiles[WOOD][0])
                    self.wood_group.add(wood)
                elif self.layout[y][x] == BRICK:
                    brick = BaseSprite(self.center_pt, self.map_tiles[BRICK][0])
                    self.brick_group.add(brick)
                elif self.layout[y][x] == CHEST:
                    chest = BaseSprite(self.center_pt, self.map_tiles[CHEST][0])
                    self.chest_group.add(chest)
                elif self.layout[y][x] == DOOR:
                    door = BaseSprite(self.center_pt, self.map_tiles[DOOR][0])
                    self.door_group.add(door)
                elif self.layout[y][x] == BRICK_STAIR_DOWN:
                    brick_stair_down = BaseSprite(self.center_pt, self.map_tiles[
                        BRICK_STAIR_DOWN][0])
                    self.brick_stair_down_group.add(brick_stair_down)
                elif self.layout[y][x] == BRICK_STAIR_UP:
                    brick_stair_up = BaseSprite(self.center_pt, self.map_tiles[
                        BRICK_STAIR_UP][0])
                    self.brick_stair_up_group.add(brick_stair_up)
                elif self.layout[y][x] == BARRIER:
                    barrier = BaseSprite(self.center_pt, self.map_tiles[
                        BARRIER][0])
                    self.barrier_group.add(barrier)
                elif self.layout[y][x] == WEAPON_SIGN:
                    weapon_sign = BaseSprite(self.center_pt, self.map_tiles[
                        WEAPON_SIGN][0])
                    self.weapon_sign_group.add(weapon_sign)
                elif self.layout[y][x] == INN_SIGN:
                    inn_sign = BaseSprite(self.center_pt, self.map_tiles[
                        INN_SIGN][0])
                    self.inn_sign_group.add(inn_sign)
                elif self.layout[y][x] == CASTLE:
                    castle = BaseSprite(self.center_pt, self.map_tiles[0][1])
                    self.castle_group.add(castle)
                elif self.layout[y][x] == TOWN:
                    town = BaseSprite(self.center_pt, self.map_tiles[1][1])
                    self.town_group.add(town)
                elif self.layout[y][x] == GRASS:
                    grass = BaseSprite(self.center_pt, self.map_tiles[2][1])
                    self.grass_group.add(grass)
                elif self.layout[y][x] == TREES:
                    trees = BaseSprite(self.center_pt, self.map_tiles[3][1])
                    self.trees_group.add(trees)
                elif self.layout[y][x] == HILLS:
                    hills = BaseSprite(self.center_pt, self.map_tiles[4][1])
                    self.hills_group.add(hills)
                elif self.layout[y][x] == MOUNTAINS:
                    mountains = BaseSprite(self.center_pt, self.map_tiles[5][1])
                    self.mountains_group.add(mountains)
                elif self.layout[y][x] == CAVE:
                    cave = BaseSprite(self.center_pt, self.map_tiles[6][1])
                    self.cave_group.add(cave)
                elif self.layout[y][x] == GRASS_STAIR_DOWN:
                    grass_stair_down = BaseSprite(self.center_pt, self.map_tiles[7][1])
                    self.grass_stair_down_group.add(grass_stair_down)
                elif self.layout[y][x] == SAND:
                    sand = BaseSprite(self.center_pt, self.map_tiles[8][1])
                    self.sand_group.add(sand)
                elif self.layout[y][x] == MARSH:
                    marsh = BaseSprite(self.center_pt, self.map_tiles[9][1])
                    self.marsh_group.add(marsh)
                elif self.layout[y][x] == BRIDGE:
                    bridge = BaseSprite(self.center_pt, self.map_tiles[10][1])
                    self.bridge_group.add(bridge)
                elif self.layout[y][x] == WATER:
                    water = BaseSprite(self.center_pt, self.map_tiles[0][2])
                    self.water_group.add(water)
                elif self.layout[y][x] == BOTTOM_COAST:
                    bottom_coast = BaseSprite(self.center_pt, self.map_tiles[1][2])
                    self.bottom_coast_group.add(bottom_coast)
                elif self.layout[y][x] == BOTTOM_LEFT_COAST:
                    bottom_left_coast = BaseSprite(self.center_pt, self.map_tiles[2][2])
                    self.bottom_left_coast_group.add(bottom_left_coast)
                elif self.layout[y][x] == LEFT_COAST:
                    left_coast = BaseSprite(self.center_pt, self.map_tiles[3][2])
                    self.left_coast_group.add(left_coast)
                elif self.layout[y][x] == TOP_LEFT_COAST:
                    top_left_coast = BaseSprite(self.center_pt, self.map_tiles[4][2])
                    self.top_left_coast_group.add(top_left_coast)
                elif self.layout[y][x] == TOP_COAST:
                    top_coast = BaseSprite(self.center_pt, self.map_tiles[5][2])
                    self.top_coast_group.add(top_coast)
                elif self.layout[y][x] == TOP_RIGHT_COAST:
                    top_right_coast = BaseSprite(self.center_pt, self.map_tiles[6][2])
                    self.top_right_coast_group.add(top_right_coast)
                elif self.layout[y][x] == RIGHT_COAST:
                    right_coast = BaseSprite(self.center_pt, self.map_tiles[7][2])
                    self.right_coast_group.add(right_coast)
                elif self.layout[y][x] == BOTTOM_RIGHT_COAST:
                    bottom_right_coast = BaseSprite(self.center_pt, self.map_tiles[8][2])
                    self.bottom_right_coast_group.add(bottom_right_coast)
                elif self.layout[y][x] == BOTTOM_TOP_LEFT_COAST:
                    bottom_top_left_coast = BaseSprite(self.center_pt, self.map_tiles[9][2])
                    self.bottom_top_left_coast_group.add(bottom_top_left_coast)
                elif self.layout[y][x] == BOTTOM_TOP_COAST:
                    bottom_top_coast = BaseSprite(self.center_pt, self.map_tiles[10][2])
                    self.bottom_top_coast_group.add(bottom_top_coast)
                elif self.layout[y][x] == BOTTOM_TOP_RIGHT_COAST:
                    bottom_top_right_coast = BaseSprite(self.center_pt, self.map_tiles[11][2])
                    self.bottom_top_right_coast_group.add(bottom_top_right_coast)

                elif self.layout[y][x] == HERO:
                    # Make player start facing up if in Tantegel Throne Room, else face down.
                    if isinstance(current_loaded_map, TantegelThroneRoom):
                        self.player_up(self.center_pt)
                    else:
                        self.player_down(self.center_pt)
                    brick = BaseSprite(self.center_pt, self.map_tiles[BRICK][0])
                    self.brick_group.add(brick)

        self.player_sprites = RenderUpdates(self.player)

    def player_down(self, center_pt):
        self.player = Player(center_pt, 0,
                             self.hero_images[0],
                             self.hero_images[1],
                             self.hero_images[2],
                             self.hero_images[3])

    def player_right(self, center_pt):
        self.player = Player(center_pt, 3,
                             self.hero_images[0],
                             self.hero_images[1],
                             self.hero_images[2],
                             self.hero_images[3])

    def player_up(self, center_pt):
        self.player = Player(center_pt, 2,
                             self.hero_images[0],
                             self.hero_images[1],
                             self.hero_images[2],
                             self.hero_images[3])

    def player_left(self, center_pt):
        self.player = Player(center_pt, 1,
                             self.hero_images[0],
                             self.hero_images[1],
                             self.hero_images[2],
                             self.hero_images[3])

    def draw_map(self, surface):
        """
        Draw static npc_sprites on the big map.
        """
        for group in self.tile_groups:
            group.draw(surface)

    def clear_sprites(self, screen, surface):
        self.player_sprites.clear(screen, surface)
        for sprite in self.npc_sprites:
            if sprite is not None:
                sprite.clear(screen, surface)

    def animate(self):
        self.player.animate()
        # TODO: Implement an extensible version of animate() which animates all npcs in the self.npcs array.
        # for npc in self.npcs:
        #    try:
        #        npc.animate()
        #    except AttributeError:
        #        print("Did not work")

    def draw_sprites(self, surface):
        self.player_sprites.draw(surface)
        for sprite in self.npc_sprites:
            if sprite is not None:
                sprite.draw(surface)


class TantegelThroneRoom(DragonWarriorMap):
    """
    This is the first map in the game.
    """

    def __init__(self, map_tiles, hero_images=None, king_lorik_images=None, left_guard_images=None,
                 right_guard_images=None, roaming_guard_images=None):
        super().__init__(map_tiles, hero_images)
        self.current_map = TantegelThroneRoom

        self.king_lorik_sprites = RenderUpdates()
        if king_lorik_images is None:
            king_lorik_images = []
        self.king_lorik_images = king_lorik_images
        self.king_lorik = AnimatedSprite

        self.left_guard_sprites = RenderUpdates()
        if left_guard_images is None:
            left_guard_images = []
        self.left_guard_images = left_guard_images
        self.left_guard = AnimatedSprite

        self.right_guard_sprites = RenderUpdates()
        if right_guard_images is None:
            right_guard_images = []
        self.right_guard_images = right_guard_images
        self.right_guard = AnimatedSprite

        self.roaming_guard_sprites = RenderUpdates()
        if roaming_guard_images is None:
            roaming_guard_images = []
        self.roaming_guard_images = roaming_guard_images
        self.roaming_guard = AnimatedSprite

        self.map_tiles = map_tiles

        if hero_images is None:
            hero_images = []
        self.hero_images = hero_images
        self.player = None

        self.roaming_characters = []
        self.center_pt = None

        self.roaming_guard = None
        self.player_sprites = None
        self.last_map = None
        self.npc_sprites = [self.king_lorik_sprites, self.left_guard_sprites, self.right_guard_sprites,
                            self.roaming_guard_sprites]
        self.npcs = [self.king_lorik, self.left_guard, self.right_guard, self.roaming_guard]
        self.layout = tantegel_throne_room
        self.width = len(self.layout[0] * TILE_SIZE)
        self.height = len(self.layout * TILE_SIZE)
        self.bgm = join(game.Game.MUSIC_DIR, '02_Dragon_Quest_1_-_Tantegel_Castle_(22khz_mono).ogg')
        pygame.mixer.music.load(self.bgm)
        # pygame.mixer.music.play(-1)

    def load_map(self):
        current_loaded_map = self

        x_offset = TILE_SIZE / 2
        y_offset = TILE_SIZE / 2

        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                self.center_pt = [(x * TILE_SIZE) + x_offset,
                                  (y * TILE_SIZE) + y_offset]
                brick = BaseSprite(self.center_pt, self.map_tiles[BRICK][0])
                brick_stair_down = BaseSprite(self.center_pt, self.map_tiles[BRICK_STAIR_DOWN][0])
                if self.layout[y][x] == ROOF:
                    roof = BaseSprite(self.center_pt, self.map_tiles[ROOF][0])
                    self.roof_group.add(roof)
                elif self.layout[y][x] == WALL:
                    wall = BaseSprite(self.center_pt, self.map_tiles[WALL][0])
                    self.wall_group.add(wall)
                elif self.layout[y][x] == WOOD:
                    wood = BaseSprite(self.center_pt, self.map_tiles[WOOD][0])
                    self.wood_group.add(wood)
                elif self.layout[y][x] == BRICK:
                    self.brick_group.add(brick)
                elif self.layout[y][x] == CHEST:
                    chest = BaseSprite(self.center_pt, self.map_tiles[CHEST][0])
                    self.chest_group.add(chest)
                elif self.layout[y][x] == DOOR:
                    door = BaseSprite(self.center_pt, self.map_tiles[DOOR][0])
                    self.door_group.add(door)
                elif self.layout[y][x] == BRICK_STAIR_DOWN:
                    self.brick_stair_down_group.add(brick_stair_down)
                elif self.layout[y][x] == HERO:
                    # Make player start facing up if in Tantegel Throne Room, else face down.
                    if isinstance(current_loaded_map, TantegelThroneRoom):
                        self.player_up(self.center_pt)
                    else:
                        self.player_down(self.center_pt)
                    if self.last_map is None:
                        self.brick_group.add(brick)
                    elif self.last_map == TantegelCourtyard:
                        self.brick_stair_down_group.add(brick_stair_down)
                elif self.layout[y][x] == KING_LORIK:
                    self.king_lorik = AnimatedSprite(self.center_pt, 0,
                                                     self.king_lorik_images[0])
                    self.king_lorik_sprites.add(self.king_lorik)
                    self.brick_group.add(brick)
                elif self.layout[y][x] == LEFT_GUARD:
                    self.left_guard = AnimatedSprite(self.center_pt, 0,
                                                     self.left_guard_images[0])
                    self.left_guard_sprites.add(self.left_guard)
                    self.brick_group.add(brick)
                elif self.layout[y][x] == RIGHT_GUARD:
                    self.right_guard = AnimatedSprite(self.center_pt, 0,
                                                      self.right_guard_images[0])
                    self.right_guard_sprites.add(self.right_guard)
                    self.brick_group.add(brick)
                elif self.layout[y][x] == ROAMING_GUARD:
                    self.roaming_guard = AnimatedSprite(self.center_pt, 0,
                                                        self.roaming_guard_images[0])
                    self.roaming_guard_sprites.add(self.roaming_guard)
                    self.roaming_characters.append(self.roaming_guard)
                    self.brick_group.add(brick)

        self.player_sprites = RenderUpdates(self.player)

    def animate(self):
        self.player.animate()
        self.king_lorik.animate()
        self.left_guard.animate()
        self.right_guard.animate()
        self.roaming_guard.animate()

    # def draw_map(self, surface):
    #    """
    #    Draw static npc_sprites on the big map.
    #    """
    #    for group in self.tile_groups:
    #        group.draw(surface)


class TantegelCourtyard(DragonWarriorMap):
    """
    This is the lower level of the first map in the game.
    """

    def __init__(self, map_tiles, hero_images=None, left_guard_images=None, right_guard_images=None,
                 roaming_guard_images=None):

        super().__init__(map_tiles, hero_images)
        self.current_map = TantegelCourtyard

        self.left_guard_sprites = RenderUpdates()
        if left_guard_images is None:
            left_guard_images = []
        self.left_guard_images = left_guard_images
        self.left_guard = None

        self.right_guard_sprites = RenderUpdates()
        if right_guard_images is None:
            right_guard_images = []
        self.right_guard_images = right_guard_images
        self.right_guard = None

        self.roaming_guard_sprites = RenderUpdates()
        if roaming_guard_images is None:
            roaming_guard_images = []
        self.roaming_guard_images = roaming_guard_images
        self.roaming_guard = None

        self.npcs = [self.left_guard, self.right_guard, self.roaming_guard]
        self.layout = tantegel_courtyard
        self.width = len(self.layout[0] * TILE_SIZE)
        self.height = len(self.layout * TILE_SIZE)

        self.bgm = join(game.Game.MUSIC_DIR, '03_Dragon_Quest_1_-_Tantegel_Castle_(Lower)_(22khz_mono).ogg')
        pygame.mixer.music.load(self.bgm)
        # pygame.mixer.music.play(-1)

    def load_map(self):

        # Currently needs to override the parent class DragonWarriorMap's load_map to allow player_right to be called.
        # May need changing later to implement correct orientation upon entering the castle from outside.

        x_offset = TILE_SIZE / 2
        y_offset = TILE_SIZE / 2

        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                self.center_pt = [(x * TILE_SIZE) + x_offset,
                                  (y * TILE_SIZE) + y_offset]
                brick = BaseSprite(self.center_pt, self.map_tiles[BRICK][0])
                brick_stair_up = BaseSprite(self.center_pt, self.map_tiles[BRICK_STAIR_UP][0])
                if self.layout[y][x] == ROOF:
                    roof = BaseSprite(self.center_pt, self.map_tiles[ROOF][0])
                    self.roof_group.add(roof)
                elif self.layout[y][x] == WALL:
                    wall = BaseSprite(self.center_pt, self.map_tiles[WALL][0])
                    self.wall_group.add(wall)
                elif self.layout[y][x] == WOOD:
                    wood = BaseSprite(self.center_pt, self.map_tiles[WOOD][0])
                    self.wood_group.add(wood)
                elif self.layout[y][x] == BRICK:
                    self.brick_group.add(brick)
                elif self.layout[y][x] == CHEST:
                    chest = BaseSprite(self.center_pt, self.map_tiles[CHEST][0])
                    self.chest_group.add(chest)
                elif self.layout[y][x] == DOOR:
                    door = BaseSprite(self.center_pt, self.map_tiles[DOOR][0])
                    self.door_group.add(door)
                elif self.layout[y][x] == BRICK_STAIR_DOWN:
                    brick_stair_down = BaseSprite(self.center_pt, self.map_tiles[
                        BRICK_STAIR_DOWN][0])
                    self.brick_stair_down_group.add(brick_stair_down)
                elif self.layout[y][x] == BRICK_STAIR_UP:
                    self.brick_stair_up_group.add(brick_stair_up)
                elif self.layout[y][x] == BARRIER:
                    barrier = BaseSprite(self.center_pt, self.map_tiles[BARRIER][0])
                    self.barrier_group.add(barrier)
                elif self.layout[y][x] == GRASS:
                    grass = BaseSprite(self.center_pt, self.map_tiles[2][1])
                    self.grass_group.add(grass)
                elif self.layout[y][x] == TREES:
                    trees = BaseSprite(self.center_pt, self.map_tiles[3][1])
                    self.trees_group.add(trees)
                elif self.layout[y][x] == HILLS:
                    hills = BaseSprite(self.center_pt, self.map_tiles[4][1])
                    self.hills_group.add(hills)
                elif self.layout[y][x] == MOUNTAINS:
                    mountains = BaseSprite(self.center_pt, self.map_tiles[5][1])
                    self.mountains_group.add(mountains)
                elif self.layout[y][x] == CAVE:
                    cave = BaseSprite(self.center_pt, self.map_tiles[6][1])
                    self.cave_group.add(cave)
                elif self.layout[y][x] == GRASS_STAIR_DOWN:
                    grass_stair_down = BaseSprite(self.center_pt, self.map_tiles[7][1])
                    self.grass_stair_down_group.add(grass_stair_down)
                elif self.layout[y][x] == SAND:
                    sand = BaseSprite(self.center_pt, self.map_tiles[8][1])
                    self.sand_group.add(sand)
                elif self.layout[y][x] == MARSH:
                    marsh = BaseSprite(self.center_pt, self.map_tiles[9][1])
                    self.marsh_group.add(marsh)
                elif self.layout[y][x] == BRIDGE:
                    bridge = BaseSprite(self.center_pt, self.map_tiles[10][1])
                    self.bridge_group.add(bridge)
                elif self.layout[y][x] == WATER:
                    water = BaseSprite(self.center_pt, self.map_tiles[0][2])
                    self.water_group.add(water)
                elif self.layout[y][x] == BOTTOM_COAST:
                    bottom_coast = BaseSprite(self.center_pt, self.map_tiles[1][2])
                    self.bottom_coast_group.add(bottom_coast)
                elif self.layout[y][x] == BOTTOM_LEFT_COAST:
                    bottom_left_coast = BaseSprite(self.center_pt, self.map_tiles[2][2])
                    self.bottom_left_coast_group.add(bottom_left_coast)
                elif self.layout[y][x] == LEFT_COAST:
                    left_coast = BaseSprite(self.center_pt, self.map_tiles[3][2])
                    self.left_coast_group.add(left_coast)
                elif self.layout[y][x] == TOP_LEFT_COAST:
                    top_left_coast = BaseSprite(self.center_pt, self.map_tiles[4][2])
                    self.top_left_coast_group.add(top_left_coast)
                elif self.layout[y][x] == TOP_COAST:
                    top_coast = BaseSprite(self.center_pt, self.map_tiles[5][2])
                    self.top_coast_group.add(top_coast)
                elif self.layout[y][x] == TOP_RIGHT_COAST:
                    top_right_coast = BaseSprite(self.center_pt, self.map_tiles[6][2])
                    self.top_right_coast_group.add(top_right_coast)
                elif self.layout[y][x] == RIGHT_COAST:
                    right_coast = BaseSprite(self.center_pt, self.map_tiles[7][2])
                    self.right_coast_group.add(right_coast)
                elif self.layout[y][x] == BOTTOM_RIGHT_COAST:
                    bottom_right_coast = BaseSprite(self.center_pt, self.map_tiles[8][2])
                    self.bottom_right_coast_group.add(bottom_right_coast)
                elif self.layout[y][x] == BOTTOM_TOP_LEFT_COAST:
                    bottom_top_left_coast = BaseSprite(self.center_pt, self.map_tiles[9][2])
                    self.bottom_top_left_coast_group.add(bottom_top_left_coast)
                elif self.layout[y][x] == BOTTOM_TOP_COAST:
                    bottom_top_coast = BaseSprite(self.center_pt, self.map_tiles[10][2])
                    self.bottom_top_coast_group.add(bottom_top_coast)
                elif self.layout[y][x] == BOTTOM_TOP_RIGHT_COAST:
                    bottom_top_right_coast = BaseSprite(self.center_pt, self.map_tiles[11][2])
                    self.bottom_top_right_coast_group.add(bottom_top_right_coast)
                elif self.layout[y][x] == HERO:
                    self.player_right(self.center_pt)
                    self.brick_stair_up_group.add(brick_stair_up)
                elif self.layout[y][x] == LEFT_GUARD:
                    self.left_guard = AnimatedSprite(self.center_pt, 0, self.left_guard_images[0])
                    self.left_guard_sprites.add(self.left_guard)
                    self.brick_group.add(brick)
                elif self.layout[y][x] == RIGHT_GUARD:
                    self.right_guard = AnimatedSprite(self.center_pt, 0, self.right_guard_images[0])
                    self.right_guard_sprites.add(self.right_guard)
                    self.brick_group.add(brick)
                elif self.layout[y][x] == ROAMING_GUARD:
                    self.roaming_guard = AnimatedSprite(self.center_pt, 0, self.roaming_guard_images[0])
                    self.roaming_guard_sprites.add(self.roaming_guard)
                    self.roaming_characters.append(self.roaming_guard)
                    self.brick_group.add(brick)
        self.player_sprites = RenderUpdates(self.player)

    def animate(self):
        self.player.animate()
        self.left_guard.animate()
        self.right_guard.animate()
        self.roaming_guard.animate()

    # def draw_map(self, surface):
    #    """
    #    Draw static npc_sprites on the big map.
    #    """
    #    for group in self.tile_groups:
    #        group.draw(surface)


class Overworld(DragonWarriorMap):
    """
    Overworld map.
    """

    def __init__(self, map_tiles, hero_images=None):
        super().__init__(map_tiles, hero_images)
        self.current_map = Overworld

        self.layout = overworld
        self.width = len(self.layout[0] * TILE_SIZE)
        self.height = len(self.layout * TILE_SIZE)

        self.bgm = join(game.Game.MUSIC_DIR, '05 Dragon Quest 1 - Kingdom of Alefgard (22khz mono).ogg')
        pygame.mixer.music.load(self.bgm)
        # pygame.mixer.music.play(-1)
