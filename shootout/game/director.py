import random
import arcade
import os
import constants
from enemy import Enemy

from shooter import Shooter


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


class Director(arcade.Window):
    def __init__(self, width, height, title):

        # calll the parent class constructor
        super().__init__(width, height, title)

        # counts in which loop to create new enemies in a regular period.
        # self.loop_counter = []

        self.all_sprites = arcade.SpriteList()
        self.shooter_sprite = None
        self.enemy_list = None
        # Keep playing
        self.keep_playing = True

    def setup(self):
        # Load background image
        # arcade.set_background_color(arcade.color.YELLOW)
        self.background = None
        self.background = arcade.load_texture("images/desert_bg.png")

        # Sprite lists

        # Set up the shooter... This will be a cowboy for now.  Might change motif later depending on sprite
        # availability and game look and feel in terms of shooter rotation rendering

        self.shooter_sprite = Shooter("images/cowboy.png", constants.SCALING)
        self.enemy_list = arcade.SpriteList()
        self.shooter_sprite.center_x = 50
        self.shooter_sprite.center_y = 50
        self.all_sprites.append(self.shooter_sprite)

        for i in range(3):

            # Create the enemy instance...  Western outlaw badguy for now...
            # This will inherit from the actor class in the next release

            enemy = Enemy("images/badguy.png",
                          constants.SCALING)

            # set default enemy x, y coordinates

            enemy.center_x = random.randrange(constants.SCREEN_WIDTH)
            enemy.center_y = random.randrange(constants.SCREEN_HEIGHT)
            enemy.change_x = random.randrange(-3, 4)
            enemy.change_y = random.randrange(-3, 4)

            # append enemy object to the master list and the enemy specific list

            self.all_sprites.append(enemy)
            self.enemy_list.append(enemy)

    def on_draw(self):

        arcade.start_render()

        # draw background image
        arcade.draw_lrwh_rectangle_textured(
            0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.background)
        # render environment using arcade magic!

        # render shooter and enemy

        self.all_sprites.draw()

    def on_update(self, delta_time):

        self.all_sprites.update()

    def on_key_press(self, key, modifiers):

        # If the user presses a key, update the speed
        if key == arcade.key.UP:
            self.shooter_sprite.change_y = constants.MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.shooter_sprite.change_y = -constants.MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.shooter_sprite.change_x = -constants.MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.shooter_sprite.change_x = constants.MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        # If a shooter releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.shooter_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.shooter_sprite.change_x = 0

# Future user mouse movement will control with click/hold/drag.  We will incorporate drag functionality in the next release
# def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
#        pass
#    def on_mouse_leave(self, x, y):
#        pass

# This is how the user mouse movement is aligned with the sprite.  The sprite will follow the mouse movement
# however the sprite can also be moved by the arrow keys

    def on_mouse_motion(self, x, y, dx, dy):
        self.shooter_sprite.center_x = x
        self.shooter_sprite.center_y = y

# for our initial release, the shooter moves diagonally down/left when left mouse button is pressed
# shooter moves diagonally up/right when right mouse button is pressed
# This will change to either rotation for aiming and/or firing bullets and other projectiles in next release

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shooter_sprite.change_x = -1
            self.shooter_sprite.change_y = -1
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.shooter_sprite.change_x = 1
            self.shooter_sprite.change_y = 1

# User mouse release will control differnt future sprite movement when we convert to a button hold event in the
# next release to allow the mouse to drag the sprite around the screen

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shooter_sprite.change_x = 0
            self.shooter_sprite.change_y = 0


# def main():
#    window = Director(constants.SCREEN_WIDTH,
#                      constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
#    window.setup()
#    arcade.run()


# if __name__ == "__main__":
#    main()
