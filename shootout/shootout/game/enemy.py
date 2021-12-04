import arcade
import constants


class Enemy(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):

        # Random enemey object movements are random for now.  this will be changed
        # significantly to more intelligent enemey movements in later release

        self.center_x += self.change_x
        self.center_y += self.change_y

        # If object hits window boundary then reverese direction
        if self.left < 0:
            self.change_x *= -1

        if self.right > constants.SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > constants.SCREEN_HEIGHT:
            self.change_y *= -1
