import random
import arcade
import os
import constants
from enemy import Enemy
import math
from constants import MOVEMENT_SPEED
from director import Director


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

# Inherits from the arcade.View class
# Initializes menu and opening splash screen with game instructions 
class Start(arcade.View):
    def __init__(self):

        # calll the parent class constructor
        super().__init__()
        # count the frames
        self.fr = 0

        # variable for background of the instruction page
        self.background = None

        # variable for background of the start presentation
        self.background2 = None

        # variable for background of the scene selection
        self.background3 = None

        # variable for the button
        self.button = None

        # variable for the mouse
        self.mouse = None

        # variable for first scenario image
        self.scenario1 = None

        # variable for second scenario image
        self.scenario2 = None

        # variable for third scenario image
        self.scenario3 = None

        # variable to save the list of sprites
        self.all_sprites = arcade.SpriteList()

        # variable that will save a number that represents the page we will be on
        self.instructions = 0

        # variable that saves the last x of the click
        self.mouse_click_x = None

        # variable that saves the last y of the click
        self.mouse_click_y = None

        # variable that saves the scenario that the Director will display. By default is number 1
        self.choose_scenario = 1

    def on_show(self):
        # giving the image to the instuctions page
        self.background = arcade.load_texture("images/menu/instructions.jpg")

        # giving the image to the start page
        self.background2 = arcade.load_texture("images/menu/welcome.jpg")

        # giving the image to the scenario page
        self.background3 = arcade.load_texture("images/menu/scenario.jpg")

        # giving the image to the button and the correct possition
        self.button = arcade.Sprite(
            "images/menu/button.png", constants.SCALING)
        self.button.center_x = 400
        self.button.center_y = 100

        # giving the image to the mouse sprite and declaring variables for it possition
        self.mouse = arcade.Sprite("images/menu/mouse.png", constants.SCALING)
        self.mouse.center_x = 0
        self.mouse.center_y = 0

        # creatinf the sprite for the first scenario possibility
        self.scenario1 = arcade.Sprite(
            "images/menu/background1.jpg", constants.SCALING)
        self.scenario1.center_x = 150
        self.scenario1.center_y = 350

        # creatinf the sprite for the second scenario possibility
        self.scenario2 = arcade.Sprite(
            "images/menu/background2.jpg", constants.SCALING)
        self.scenario2.center_x = 400
        self.scenario2.center_y = 350

        # creating the sprite for the third scenario possibility
        self.scenario3 = arcade.Sprite(
            "images/menu/background3.jpg", constants.SCALING)
        self.scenario3.center_x = 650
        self.scenario3.center_y = 350

    def on_draw(self):
        # starting rendering the game
        arcade.start_render()

        # the presentation page will be shown for 100 frames
        if self.fr < 100:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.background2)

        # after 100 frames the instruction page will be shown
        else:
            # the instruction variable is by default 0 so will call the correct page
            if self.instructions == 0:
                arcade.draw_lrwh_rectangle_textured(
                    0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.background)

            # after clicking at the instruction page, the instruction variable will change to 1 so will call the next page
            else:
                arcade.draw_lrwh_rectangle_textured(
                    0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.background3)

            # drawing the sprites, the mouse has to be at last
            self.all_sprites.draw()
            self.mouse.draw()

    def on_update(self, delta_time):
        # changing the size of the button if the mouse is above to make it appealing to the user
        if (self.mouse.center_x in range((self.button.center_x)-75, (self.button.center_x)+75)) and (self.mouse.center_y in range((self.button.center_y)-50, (self.button.center_y)+50)):
            self.button.width = 180
            self.button.height = 180

        # when the mouse goes out the size returns to its normal
        else:
            self.button.width = 150
            self.button.height = 150

        # changing the size of the first scenario if the mouse is above to make it appealing to the user
        if (self.mouse.center_x in range((self.scenario1.center_x)-100, (self.scenario1.center_x)+100)) and (self.mouse.center_y in range((self.scenario1.center_y)-80, (self.scenario1.center_y)+80)):
            self.scenario1.width = 220
            self.scenario1.height = 165

        # if the mouse goes out it returns to its normal size, but if it was clicked it stays bigger
        else:
            if (self.mouse_click_x not in range((self.scenario1.center_x)-100, (self.scenario1.center_x)+100)) or (self.mouse_click_y not in range((self.scenario1.center_y)-80, (self.scenario1.center_y)+80)):
                self.scenario1.width = 200
                self.scenario1.height = 150

            # we save the number of the scenario selected. In the future we will send this information to the director to apply the textures
            else:
                self.choose_scenario = 1

        # changing the size of the second scenario if the mouse is above to make it appealing to the user
        if (self.mouse.center_x in range((self.scenario2.center_x)-100, (self.scenario2.center_x)+100)) and (self.mouse.center_y in range((self.scenario2.center_y)-80, (self.scenario2.center_y)+80)):
            self.scenario2.width = 220
            self.scenario2.height = 165

        # if the mouse goes out it returns to its normal size, but if it was clicked it stays bigger
        else:
            if (self.mouse_click_x not in range((self.scenario2.center_x)-100, (self.scenario2.center_x)+100)) or (self.mouse_click_y not in range((self.scenario2.center_y)-80, (self.scenario2.center_y)+80)):
                self.scenario2.width = 200
                self.scenario2.height = 150

            # we save the number of the scenario selected. In the future we will send this information to the director to apply the textures
            else:
                self.choose_scenario = 2

        # changing the size of the third scenario if the mouse is above to make it appealing to the user
        if (self.mouse.center_x in range((self.scenario3.center_x)-100, (self.scenario3.center_x)+100)) and (self.mouse.center_y in range((self.scenario3.center_y)-80, (self.scenario3.center_y)+80)):
            self.scenario3.width = 220
            self.scenario3.height = 165

        # if the mouse goes out it returns to its normal size, but if it was clicked it stays bigger
        else:
            if (self.mouse_click_x not in range((self.scenario3.center_x)-100, (self.scenario3.center_x)+100)) or (self.mouse_click_y not in range((self.scenario3.center_y)-80, (self.scenario3.center_y)+80)):
                self.scenario3.width = 200
                self.scenario3.height = 150

            # we save the number of the scenario selected. In the future we will send this information to the director to apply the textures
            else:
                self.choose_scenario = 3

        # if the start button is clicked we will create the director instance to start the game
        if (self.mouse_click_x in range((self.button.center_x)-75, (self.button.center_x)+75)) and (self.mouse_click_y in range((self.button.center_y)-50, (self.button.center_y)+50)):

            # the director recives a variable with the number of the scenario that the user selected last
            game_view = Director(self.choose_scenario)
            self.window.show_view(game_view)

            # making the mouse visible again
            self.window.set_mouse_visible(True)

        # counting the frames
        self.fr += 1

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the mouse sprite to match the mouse x, y
        self.mouse.center_x = x
        self.mouse.center_y = y - 10

    def on_mouse_press(self, x, y, _button, _modifiers):

        # with the next if we not let the user change something with the click at the start of the game
        # at the instruction page if the user clicks will be sent to the scenarios page
        if (self.fr > 100) and (self.instructions == 0):
            self.instructions = 1
            self.all_sprites.append(self.button)
            self.all_sprites.append(self.scenario1)
            self.all_sprites.append(self.scenario2)
            self.all_sprites.append(self.scenario3)

        # if we are at the scenarios page will will save the position of the last click
        elif self.instructions == 1:
            self.mouse_click_x = x
            self.mouse_click_y = y
