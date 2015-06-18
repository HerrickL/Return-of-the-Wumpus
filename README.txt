Return of the Wumpus  by Lynn Herrick

Libraries required
------------------

pygame, matplotlib, setuptools, simpleGUICS2Pygame, random

http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib
http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools
https://pypi.python.org/pypi/SimpleGUICS2Pygame

Other requirements
------------------

This game requires audio


Description
-----------

Based off of the 1972 game, "Hunt the Wumpus", Return of the Wumpus places a player in a cave with collectables and baddies.  To start, click in the box that says "click to start'. The player can move up/down/left/right using the arrow keys on their keyboard.  With each move, the player will sense if there is anything good or bad in adjacent cave-rooms.  Glittering indicates money or an extra bullet is near.  Wind indicates a hole is near.  Bandits indicate bandits are near.  The wumpus indicates that the wumpus is near.  The hole causes the player to fall back to the starting position.  The player can shoot if they sense the bandits or wumpus to be near.  The 'w' shoots up, the 'a' shoots left, the 's' shoots down, and the 'd' shoots right.  Shots will be fired only into adjacent rooms of the chosen direction.  If the player has guessed the correct position of the bandits or wumpus, the bandits or wumpus will die.  If a shot is fired and the wumpus is not dead, even if it is a shot that hits bandits, the wumpus will move positions on the board.  This could result in the wumpus finding your position and eating you. This only relates to the wumpus, the bandits will not change positions for any reason.  If you enter the cave-room of the bandits while they are still alive, they will take your money if you have any.  If you do not have any money, they will kill you.  If you enter the cave-room of the wumpus, it will kill you.  The game ends when the player has collected the money, and killed the bandits and wumpus or if the player has died.  The maximum ammount of bullets the player has at their disposal is 3 (2 starting, plus one extra in a cave-room).  Each new game will randomize different locations for the collectables and the baddies.

Sound and Image Files
---------------------
The bullet image was created by Kim Lathrop. All other images were created by myself or released into the public domain through openclipart.org

The sound files are all obtained from soundbible.com

