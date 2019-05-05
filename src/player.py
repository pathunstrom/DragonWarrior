from src.animated_sprite import AnimatedSprite
from src.common import TILE_SIZE


class Player(AnimatedSprite):

    def __init__(self, center_point, direction, down_img, left_img, up_img,
                 right_img):
        AnimatedSprite.__init__(self, center_point, direction, down_img,
                                left_img, up_img, right_img)

    def update(self, wall_group):
        pass

    def set_center_point(self, center_point):
        self.center_point = center_point
