import arcade
import random
import time

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 690

starxpositions=[]
starypositions=[]

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)
        self._focused = True

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.starttime=time.time()
        arcade.set_background_color(arcade.color.BLACK)
        self.wraps = False

    def setup(self):
        self.star_list = arcade.SpriteList()
        self.ship = arcade.Sprite("ship.png", 1)
        self.ship.center_x = SCREEN_WIDTH / 5
        self.ship.center_y = SCREEN_HEIGHT / 2

        self.potato_list = arcade.SpriteList()
        self.potatoes=[]
        self.gameover = arcade.Sprite("gameover.png",3)
        self.gameover.center_x = SCREEN_WIDTH / 2
        self.gameover.center_y = SCREEN_HEIGHT / 2

        for i in range(30):
          star = arcade.Sprite("star.png", 0.015)
          starxpositions.append((i*20))
          starypositions.append(random.randrange(0, SCREEN_HEIGHT))
          star.center_x = starxpositions[i]
          star.center_y = starypositions[i]

          self.star_list.append(star)

        arcade.schedule(self.createPotato, 1)

        
        #self.potato.velocity = 100


        # Your drawing code goes here

    def createPotato(self, delta_time: float):
        potato = arcade.Sprite("potato.png",0.5)
        
       
        potato.center_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH*2)
        potato.center_y = random.randrange(SCREEN_HEIGHT)

        self.potato_list.append(potato)
        self.potatoes.append(random.randint(2,4))

        # arcade.unschedule(self.createPotato)
        # arcade.schedule(self.createPotato, float(random.randrange(20, 75))/100)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        if self.wraps == True:
          return
        self.ship.change_x = 0
        self.ship.change_y = 0

        for tot in self.potato_list:
          if self.ship.collides_with_sprite(tot):
            self.wraps = True
            self.endtime = str(int(time.time()-self.starttime))
            arcade.unschedule(self.createPotato)
            self.gameover.draw()
          else:
            if self.up_pressed and not self.down_pressed:
              self.ship.center_y += 1.5
            elif self.down_pressed and not self.up_pressed:
              self.ship.center_y -= 1.5

            for star in self.star_list:
              if star.center_x < 1:
                star.center_x += SCREEN_WIDTH
              else:
                star.center_x -= 1
            
            for i in range(len(self.potato_list)):
              potato = self.potato_list[i]
              potato.center_x -= self.potatoes[i]-1
              potato.angle += self.potatoes[i]

            newpotato_list=arcade.SpriteList()
            newpotatoes=[]
            for pot in range (len(self.potato_list)):
              if self.potato_list[pot].center_x >= 0:
                newpotato_list.append(self.potato_list[pot])
                newpotatoes.append(self.potatoes[pot])
            self.potatoes=newpotatoes
            self.potato_list=newpotato_list
      
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False


    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        self.star_list.draw()
        if self.wraps:
          self.gameover.draw()
          for i in range(3):
            arcade.draw_text("SCORE: "+self.endtime, ((SCREEN_WIDTH*9)/20)+i, SCREEN_HEIGHT/2,arcade.color.BLACK, 12, anchor_x="left", anchor_y="top", bold=True)
        self.ship.draw()  
        self.potato_list.draw() 

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
