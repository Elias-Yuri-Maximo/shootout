import arcade
import constants
from director import Director

if __name__ == "__main__":
    app = Director(constants.SCREEN_WIDTH,
                   constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    app.setup()
    arcade.run()
