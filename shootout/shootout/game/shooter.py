import arcade
import constants


# Inherits from arcade.Sprite class
class Shooter(arcade.Sprite):

    def update(self):
        # shooter positioning tracking and updates.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Set shooter movement boundaries defined by Window class attributes
        if self.left < 0:
            self.left = 0
        elif self.right > constants.SCREEN_WIDTH - 1:
            self.right = constants.SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > constants.SCREEN_HEIGHT - 1:
            self.top = constants.SCREEN_HEIGHT - 1
