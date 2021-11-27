import random
import arcade
import os
import constants
from enemy import Enemy
import math

from shooter import Shooter


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


class Director(arcade.Window):
    def __init__(self, width, height, title):

        # calll the parent class constructor
        super().__init__(width, height, title)

        # counts in which loop to create new enemies in a regular period.
        # self.loop_counter = []
        self.frame_count =0

        self.all_sprites = arcade.SpriteList()
        self.bullet_list = None
        self.shooter_sprite = None
        self.enemy_list = None

        # the heart list will save all the heart images that represents the lives of the player.
        # when the player looses a live we can remove a heart from the list easily.
        self.heart_list = None

        # Keep playing
        self.keep_playing = True
        self.score = 0

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
        self.heart_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
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

        # the next for loop will creat three hearts images to print on the screen and save them in the corresponding lists
        for i in range(3):

            # creating one heart
            heart = arcade.Sprite("images/heart.png",
                                  constants.SCALING)

            # set heart x, y coordinates
            # The heart separation is the separation between the heart images. Each of the hearts will have different x values
            # "570" is the y value and it is the same value of the Score y to make them be at the same line

            heart.center_x = 700 + constants.HEART_SEPARATION * i
            heart.center_y = 570

            # append heart object to the master list and the heart specific list

            self.all_sprites.append(heart)
            self.heart_list.append(heart)

    def on_draw(self):

        arcade.start_render()

        # draw background image
        arcade.draw_lrwh_rectangle_textured(
            0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.background)
        # render environment using arcade magic!

        # render shooter and enemy

        self.all_sprites.draw()

        # create a text at the screen that shows the Score
        # first parameter = text, second paramenter = x, third parameter = y, fourth parameter = color, fifth parameter = font size
        # if we want to update the score we can call the "self.score" at the "on_update" function and assign a new number
        arcade.draw_text(f"Score: {self.score}", 10,
                         570, arcade.color.RED, 20)


    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        # Create a bullet
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", constants.SPRITE_SCALING_LASER)

        # Position the bullet at the player's current location
        start_x = self.shooter_sprite.center_x
        start_y = self.shooter_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle) * constants.BULLET_SPEED
        bullet.change_y = math.sin(angle) * constants.BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)
        self.all_sprites.append(bullet)


    def on_update(self, delta_time):

        self.all_sprites.update()


        self.frame_count += 1
        for enemy in self.enemy_list:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
                start_x = enemy.center_x
                start_y = enemy.center_y

            # Get the destination location for the bullet
                dest_x = self.shooter_sprite.center_x
                dest_y = self.shooter_sprite.center_y
                
                # Do math to calculate how to get the bullet to the destination.
                # Calculation the angle in radians between the start points
                # and end points. This is the angle the bullet will travel.

                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)

                if self.frame_count % 120 == 0:
                    bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                    bullet.center_x = start_x
                    bullet.center_y = start_y

                    # Angle the bullet sprite
                    bullet.angle = math.degrees(angle)

                    # Taking into account the angle, calculate our change_x
                    # and change_y. Velocity is how fast the bullet travels.
                    bullet.change_x = math.cos(angle) * constants.BULLET_SPEED
                    bullet.change_y = math.sin(angle) * constants.BULLET_SPEED

                    self.bullet_list.append(bullet)
                    self.all_sprites.append(bullet)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()
                



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

    #def on_mouse_motion(self, x, y, dx, dy):
    #    self.shooter_sprite.center_x = x
    #    self.shooter_sprite.center_y = y

# for our initial release, the shooter moves diagonally down/left when left mouse button is pressed
# shooter moves diagonally up/right when right mouse button is pressed
# This will change to either rotation for aiming and/or firing bullets and other projectiles in next release

    #def on_mouse_press(self, x, y, button, modifiers):
    #    if button == arcade.MOUSE_BUTTON_LEFT:
    #        self.shooter_sprite.change_x = -1
    #        self.shooter_sprite.change_y = -1
    #    if button == arcade.MOUSE_BUTTON_RIGHT:
    #        self.shooter_sprite.change_x = 1
    #        self.shooter_sprite.change_y = 1

# User mouse release will control differnt future sprite movement when we convert to a button hold event in the
# next release to allow the mouse to drag the sprite around the screen

    #def on_mouse_release(self, x, y, button, modifiers):
    #    if button == arcade.MOUSE_BUTTON_LEFT:
    #        self.shooter_sprite.change_x = 0
    #        self.shooter_sprite.change_y = 0


# def main():
#    window = Director(constants.SCREEN_WIDTH,
#                      constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
#    window.setup()
#    arcade.run()


# if __name__ == "__main__":
#    main()
