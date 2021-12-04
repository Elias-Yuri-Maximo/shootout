import random
import arcade
import os
import constants
from enemy import Enemy
import math
from constants import MOVEMENT_SPEED, WESTERN_ASSETS, OUTERSPACE_ASSETS, FOREST_ASSETS

from shooter import Shooter


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


class Director(arcade.Window):
    def __init__(self, width, height, title):

        # calll the parent class constructor
        super().__init__(width, height, title)

        # Load background image
        self.background = None

        # counts in which loop to create new enemies in a regular period.
        # self.loop_counter = []
        self.frame_count =0


        self.all_sprites = arcade.SpriteList()
        self.bullet_list = None
        self.shooter_gun_list =None
        self.shooter_sprite = None
        self.enemy_list = None
        self.shooter_list = None

        # Movement variables. These are new. I want to optimize movement.
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        # the heart list will save all the heart images that represents the lives of the player.
        # when the player looses a live we can remove a heart from the list easily.
        self.heart_list = None

        # Keep playing
        self.keep_playing = True
        self.score = 0


 
        
        self.shooter_textures = []
        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture(os.path.join(WESTERN_ASSETS,"inverted_shooter.png"))
        self.shooter_textures.append(texture)
        texture = arcade.load_texture(os.path.join(WESTERN_ASSETS,"shooter.png"))
        self.shooter_textures.append(texture)

        self.gun_textures = []
        texture = arcade.load_texture(os.path.join(WESTERN_ASSETS,"gun.png"))
        self.gun_textures.append(texture)
        texture = arcade.load_texture(os.path.join(WESTERN_ASSETS,"inverted_gun.png"))
        self.gun_textures.append(texture)


        # By default, face right.
        
        

    def initiate_enemy(self):
        enemy = Enemy(os.path.join(WESTERN_ASSETS,"enemy.png"),
                            constants.SCALING)

            # set default enemy x, y coordinates

        enemy.center_x = random.randrange(constants.SCREEN_WIDTH)
        enemy.center_y = random.randrange(constants.SCREEN_HEIGHT)
        enemy.change_x = random.randrange(-3, 4)
        enemy.change_y = random.randrange(-3, 4)

                # append enemy object to the master list and the enemy specific list

        self.all_sprites.append(enemy)
        self.enemy_list.append(enemy)


    def setup(self):

        # arcade.set_background_color(arcade.color.YELLOW)
        self.background = arcade.load_texture(os.path.join(WESTERN_ASSETS,"background.png"))

        # Sprite lists

        # Set up the shooter... This will be a cowboy for now.  Might change motif later depending on sprite
        # availability and game look and feel in terms of shooter rotation rendering
        self.shooter_gun_sprite = Shooter(os.path.join(WESTERN_ASSETS,"gun.png"), constants.SCALING)
        self.shooter_gun_list = arcade.SpriteList()
        self.shooter_gun_list.append(self.shooter_gun_sprite)
        self.all_sprites.append(self.shooter_gun_sprite)
       
       
       
        self.shooter_sprite = Shooter(os.path.join(WESTERN_ASSETS,"shooter.png"), constants.SCALING)
        self.shooter_list = arcade.SpriteList()
        self.shooter_list.append(self.shooter_sprite)



    

        self.enemy_list = arcade.SpriteList()
        self.heart_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.shooter_bullet_list= arcade.SpriteList()
        self.shooter_sprite.center_x = 50
        self.shooter_sprite.center_y = 50
        # Sounds
        # Load sounds
        # Background music: "Uptown" by Topher Mohr and Alex Elena
        # https://www.youtube.com/watch?v=wTm-WFM0v-g&t=2517s
        #
        # In order: Gunshot, Grunt (hurt), Grunt (dead).
        #
        self.background_music = arcade.load_sound("sounds/western_bgm.mp3")
        self.gunshot_sound = arcade.load_sound("sounds/gunshot.wav")
        # future 
        # self.hurt_sound = arcade.load_sound("sounds/grunt_hurt.wav")
        # future 
        # self.dead_sound = arcade.load_sound("sounds/grunt_dead.wav")

        self.all_sprites.append(self.shooter_sprite)
        
        # In order: Gunshot, Grunt (hurt), Grunt (dead).
       
        # Start background music! (Maybe this should be put somewhere else...)
        arcade.play_sound(self.background_music)


        for i in range(3):

            # Create the enemy instance...  Western outlaw badguy for now...
            # This will inherit from the actor class in the next release

            
            self.initiate_enemy()

        # the next for loop will creat three hearts images to print on the screen and save them in the corresponding lists
        for i in range(10):

            # creating one heart
            heart = arcade.Sprite(os.path.join(WESTERN_ASSETS,"heart.png"),
                                  constants.SCALING)

            # set heart x, y coordinates
            # The heart separation is the separation between the heart images. Each of the hearts will have different x values
            # "570" is the y value and it is the same value of the Score y to make them be at the same line

            heart.center_x = 500 + constants.HEART_SEPARATION * i
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

        self.shooter_gun_sprite.draw()


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
        self.shooter_bullet_list.append(bullet)
        self.all_sprites.append(bullet)

        # Now that bullet is on screen, play the sound!
        arcade.play_sound(self.gunshot_sound) 
        start_x = self.shooter_sprite.center_x
        start_y = self.shooter_sprite.center_y





    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        
        if x > self.shooter_sprite.center_x:
            #flip the flippedy thing
            pass


        for gun in self.shooter_gun_list:

            # First, calculate the angle to the player. We could do this
                # only when the bullet fires, but in this case we will rotate
                # the enemy to face the player each frame, so we'll do this
                # each frame.
            shooter = self.shooter_list[0]

                # Position the start at the enemy's current location
            start_x = shooter.center_x
            start_y = shooter.center_y

                # Get the destination location for the bullet
            dest_x = x
            dest_y = y

                # Do math to calculate how to get the bullet to the destination.
                # Calculation the angle in radians between the start points
                # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

                # Set the enemy to face the player.
            gun.angle = math.degrees(angle) - 90

        if x > self.shooter_sprite.center_x:
            self.shooter_sprite.texture = self.shooter_textures[1]
            self.shooter_gun_sprite.texture = self.gun_textures[1]
        else:
            self.shooter_sprite.texture = self.shooter_textures[0]
            self.shooter_gun_sprite.texture = self.gun_textures[0]


        return super().on_mouse_motion(x, y, dx, dy)





    def on_update(self, delta_time):

        # This block is new, from Noah. Taken from the Python Arcade Library to optimize movement.
        # https://api.arcade.academy/en/latest/examples/sprite_move_keyboard_better.html
        
        # Now, the most recent keypress takes priority over its opposite.
        # Holding left, then holding right simultaneously, will make you go right.
        # Releasing right will then make you resume moving left.
        # This is the kind of movement that I'm used to.
        self.shooter_sprite.change_y = 0
        self.shooter_sprite.change_x = 0
        # Some of the lines below are half commented out.
        # That's me modifying the example. This way, pressing two opposite directions
        # will not cause zero movement. Instead, the most recent keypress of the two will take priority.
        if self.up_pressed:# and not self.down_pressed:
            self.shooter_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed:# and not self.up_pressed:
            self.shooter_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed:# and not self.right_pressed:
            self.shooter_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed:# and not self.left_pressed:
            self.shooter_sprite.change_x = MOVEMENT_SPEED



        self.shooter_gun_sprite.center_x = self.shooter_sprite.center_x
        self.shooter_gun_sprite.center_y = self.shooter_sprite.center_y

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
                    #self.enemy_bullet_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
                    #arcade.play_sound(self.enemy_bullet_soundenemy_bullet_sound)
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

            hit_list = arcade.check_for_collision_with_list(bullet, self.shooter_list)

            if len(hit_list) > 0:

                heart = self.heart_list[0] 
                self.heart_list.remove(heart)
                self.all_sprites.remove(heart)

                bullet.remove_from_sprite_lists()


            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        for bullet in self.shooter_bullet_list:

            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            if len(hit_list) > 0: 
                

                bullet.remove_from_sprite_lists()

                for enemy in hit_list:

                    enemy.remove_from_sprite_lists()

                    

                self.initiate_enemy()
                self.score+=10



    def on_key_press(self, key, modifiers):

        # If the user presses a key, set the appropriate flag
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

        # If a shooter releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        # if key == arcade.key.UP or key == arcade.key.DOWN:
        #     self.shooter_sprite.change_y = 0
        # elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
        #     self.shooter_sprite.change_x = 0


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
