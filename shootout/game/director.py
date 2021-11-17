from time import sleep
import arcade
import random
from game import constants
from game.actor import Actor
from game.enemy_character import EnemyCharacter
from game.handle_collision import HandleCollision
from game.bullet import Bullet
from game.input_service import InputService
from game.lives import Lives
from game.output_service import OutputService
from game.player_character import PlayerCharacter
from game.point import Point
from game.score import Score

class Director(arcade.Window): 
    def __init__(self, width, height, title):

        #calll teh parent class constructor
        super().__init__(self, width, height, title)
    
        #counts in which loop to create new enemies in a regular period.
        #self.loop_counter = []

        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()


        arcade.schedule(self.add_enemy, 0.25)
        #Keep playing
        self.keep_playing = True
        

        
    def setup(self):
        """
        Sets the window up for playing

        Args (self)
        """

        #set the background color 'to yellowish'
        arcade.set_background_color(arcade.color.YELLOW)

        self.player = arcade.Sprite("images/sun-icon.png", constants.SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)
        
    def add_enemy(self, delta_time: float):
        """Adds a new enemy to the screen

        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """

        # First, create the new enemy sprite
        enemy = arcade.Sprite("images/missile.png", SCALING)

        # Set its position to a random height and off screen right
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)

        # Set its speed to a random speed heading left
        enemy.velocity = (random.randint(-20, -5), 0)

        # Add it to the enemies list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)






  #  def on_draw(self):
  #      return super().on_draw()
        
  #  def on_key_press(self, symbol: int, modifiers: int):
  #      return super().on_key_press(symbol, modifiers)

def on_update(self, delta_time: float):
    
    for enemy in self.enemies_list:
        if enemy.right < 0:
            enemy.remove_from_sprite_lists()

    return super().on_update(delta_time)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    def start_game(self):
        




        while self.keep_playing:
            self._get_inputs()
            self._do_updates()
            self._do_outputs()
            sleep(constants.FRAME_LENGTH)

    def _get_inputs(self):
        """Gets the inputs at the beginning of each round of play. In this case,
        that means getting the desired direction and moving the snake.

        Args:
        self (Director): An instance of Director.
        """
        pass

    def _do_updates(self):
        """Does the checks to see if someone was hit
        
        Args:
        self (Director): An instance of Director
        """
        pass


    def _do_outputs(self):
        """
        Does the outputs of the game 

        Args: 
        self (Director): An instance of Director.
        """
        pass
    '''