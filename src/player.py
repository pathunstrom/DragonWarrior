from os.path import join

import pygame

import src.game
from src import common, maps
from src.animated_sprite import AnimatedSprite


class Player(AnimatedSprite):

    def __init__(self, center_point, direction, down_img, left_img, up_img,
                 right_img):
        AnimatedSprite.__init__(self, center_point, direction, down_img,
                                left_img, up_img, right_img)
        self.index = 0
        self.hero_current_location = None
        self.hero_start_location = None
        self.bump_sound_path = join(src.game.Game.SFX_DIR, '42 Dragon Quest 1 - Bumping into Walls (22khz mono).wav')
        self.bump_sound = pygame.mixer.Sound(self.bump_sound_path)

    def update(self, wall_group):
        pass
        # self.index += 1
        # if self.index >= len(self.image):
        #    self.index = 0
        # self.image = self.image[self.index]

    def get_hero_start_location(self, current_map):
        for i, e in enumerate(current_map.layout):
            if maps.HERO in e:
                try:
                    self.hero_start_location = i, e.index(maps.HERO)
                except ValueError:
                    pass
        self.hero_current_location = self.hero_start_location
        return self.hero_start_location

    def set_center_point(self, center_point):
        self.center_point = center_point

    # def render(self, display):
    # display.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, camera_pos, current_map):
        # TODO: Smooth out movement.
        pos_x, pos_y = camera_pos
        # For debugging
        print("Currently at: " + str(self.hero_current_location))
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            self.direction = AnimatedSprite.DOWN
            x_trajectory = self.hero_current_location[0] + 1
            y_trajectory = self.hero_current_location[1]
            if any(impassable_object == current_map.layout[x_trajectory][y_trajectory] for impassable_object in
                   maps.impassable_objects):
                self.bump_sound.play()
            else:
                self.rect.y += common.TILE_SIZE
                self.hero_current_location = x_trajectory, y_trajectory
                # enable this if calling player.move twice
                # (for instance, for debugging purposes while printing the coordinates of camera_pos)
                # self.rect.y += common.TILE_SIZE // 2
                pos_y -= common.TILE_SIZE
        if key[pygame.K_LEFT]:
            self.direction = AnimatedSprite.LEFT
            x_trajectory = self.hero_current_location[0]
            y_trajectory = self.hero_current_location[1] - 1
            if any(impassable_object == current_map.layout[x_trajectory][y_trajectory] for impassable_object in
                   maps.impassable_objects):
                self.bump_sound.play()
            else:
                self.rect.x -= common.TILE_SIZE
                self.hero_current_location = x_trajectory, y_trajectory
                pos_x += common.TILE_SIZE
        if key[pygame.K_UP]:
            self.direction = AnimatedSprite.UP
            x_trajectory = self.hero_current_location[0] - 1
            y_trajectory = self.hero_current_location[1]
            if any(impassable_object == current_map.layout[x_trajectory][y_trajectory] for impassable_object in
                   maps.impassable_objects):
                self.bump_sound.play()
            else:
                self.rect.y -= common.TILE_SIZE
                self.hero_current_location = x_trajectory, y_trajectory
                pos_y += common.TILE_SIZE
        if key[pygame.K_RIGHT]:
            self.direction = AnimatedSprite.RIGHT
            x_trajectory = self.hero_current_location[0]
            y_trajectory = self.hero_current_location[1] + 1
            if any(impassable_object == current_map.layout[x_trajectory][y_trajectory] for impassable_object in
                   maps.impassable_objects):
                self.bump_sound.play()
            else:
                self.rect.x += common.TILE_SIZE
                self.hero_current_location = x_trajectory, y_trajectory
                pos_x -= common.TILE_SIZE

        # TODO: Handle roaming guard sides collision (take position of roaming guard, disallow movement to that point).
        if self.rect.x < 0:  # Simple Sides Collision
            self.rect.x = 0  # Reset Player Rect Coord
            pos_x = camera_pos[0]  # Reset Camera Pos Coord
            self.hero_current_location = 0, self.hero_current_location[1]
            self.bump_sound.play()
        elif self.rect.x > int(src.game.Game.WIN_WIDTH - ((src.game.Game.WIN_WIDTH // 24) * 1.5)):
            self.rect.x = int(src.game.Game.WIN_WIDTH - ((src.game.Game.WIN_WIDTH // 24) * 1.5))
            pos_x = camera_pos[0]
            self.hero_current_location = self.hero_current_location[0] - 1, self.hero_current_location[1]
            self.bump_sound.play()
        if self.rect.y < 0:
            self.rect.y = 0
            pos_y = camera_pos[1]
            self.hero_current_location = self.hero_current_location[0], 0
            self.bump_sound.play()
        elif self.rect.y > src.game.Game.WIN_HEIGHT - 48:
            self.rect.y = src.game.Game.WIN_HEIGHT - 48
            self.hero_current_location = self.hero_current_location[0], self.hero_current_location[1] - 1
            self.bump_sound.play()
        # print(self.hero_current_location)
        elif self.rect.y > src.game.Game.WIN_HEIGHT - ((src.game.Game.WIN_HEIGHT // 23) * 1.5):
            self.rect.y = src.game.Game.WIN_HEIGHT - ((src.game.Game.WIN_HEIGHT // 23) * 1.5)

        # pos_y = camera_pos[1]
        # TODO: implement actual function of B, A, Start, Select buttons.
        if key[pygame.K_z]:
            # B button
            print("You pressed the z key.")
        if key[pygame.K_y]:
            # A button
            print("You pressed the y key.")
        if key[pygame.K_SPACE]:
            # Start button
            print("You pressed the space bar.")
        if key[pygame.K_ESCAPE]:
            # Select button
            print("You pressed the escape key.")
        return pos_x, pos_y
