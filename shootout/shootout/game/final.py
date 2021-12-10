import arcade
import os

from arcade.text_pyglet import FontNameOrNames
import constants


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

# Inherits from arcade.View class
# This class render's the final exit screen at the end of the game and draws the final score in the heading 
class Final(arcade.View):
    def __init__(self, score):

        # calll the parent class constructor
        super().__init__()

        # variable for background of the instruction page
        self.background = None

        # variable to save the list of sprites
        self.all_sprites = arcade.SpriteList()

        self.score = score

    def on_show(self):
        # provides image to the final splash page
        self.background = arcade.load_texture("images/menu/final.jpg")

    def on_draw(self):
        # refresh game view
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(
            0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.background)

        arcade.draw_text(f"Final Score:{self.score}",
                         0,
                         500,
                         arcade.color.RED,
                         40,
                         800,
                         align="center", font_name="Kenney Blocks")

        arcade.draw_text(f"Click to finish the game",
                         0,
                         50,
                         arcade.color.RED,
                         30,
                         800,
                         align="center", font_name="Freestyle Script")

    def on_mouse_press(self, x, y, _button, _modifiers):

        arcade.exit()
