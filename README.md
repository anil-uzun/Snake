The traditional snake game with a few more extra features.
# The Main Goal
The main goal is to eat the food that is scattered around the board using your snake and survive as long as possible to get the highest score.
# Features
## Controlling the snake
The snake is controlled using the arrow keys and will never stop moving unless the game is paused.  
The snake will have an initial speed of 10 which will increase as you progress.  
By holding down the space bar the snake will start sprinting by moving twice it's current speed.  
If multiple inputs are made before the snake is able to complete an action the input will be put on a queue and will be put in action as soon as the current action is completed.
## Food
There are 3 types of food that can spawn that are dependant on the max food count.
### Regular Food
This type of food is orange colored and when eaten will grow the snake 1 tile and add 1 to the players score.
### Special Foods
Special type of food will spawn everytime a players score hits a multiple of 10, if the players score passes the closest multiple of 10 without hitting it the food will still spawn.
While these types of food are on the board no additional regular food can spawn. -So the player is forced to eat them-
- ### Gold Food
  This type of food when eaten will increase the maximum amount of regular food that can be on the map by 1.  
  Every time a special food spawn event occurs gold food will have some chance of spawning that is inversely proportional to the maximum amount of regular food.  
  Only one can spawn at a time.  
  One blue food will most likely spawn alongside it.  
  When eaten will add 1 to the players score.
- ### Blue food
  This type of food when eaten will increase the players speed by 1 -the default speed is 10-.  
  Unlike the Gold food this type of food will always spawn in pairs of two  
  When eaten will add 1 to the players score.
## The Menus
- By pressing esc the player is able to pause the game and will be greeted with a pause menu. While on this screen the player can press esc again to unpause the game.
- If the snake collides with it's own body the game will be considered lost and a game over screen with a red transparent dim over the game will be displayed. While on this screen the player can press esc to quit the app or press space to restart the game.
