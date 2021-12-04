import arcade
import constants
from director import Director
from start import Start

if __name__ == "__main__":
    app = arcade.Window(constants.SCREEN_WIDTH,
                        constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    view = Start()

    # taking out the mouse to not be duplicated with the mouse sprite
    app.set_mouse_visible(False)
    app.show_view(view)
    arcade.run()
