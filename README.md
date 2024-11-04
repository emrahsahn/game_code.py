# game_code.py
Lord Of The Polywarphism
Within the scope of the project, a multiplayer war game will be developed in a 2-dimensional matrix world.

GAME DESCRIPTION

The dimensions of the 2-dimensional world will be selected at the beginning of the game. Users will be able to play the game in a user-defined world of 16x16, 24x24, or 32x32. The world's size cannot be smaller than 8x8 or larger than 32x32.

There will be a minimum of 1 real player and a maximum of 4 players in the game.

Players will take turns playing the game. When it is a player's turn, they can produce up to 2 warriors within a turn if their resources are sufficient. Warriors can be any type of warrior listed in the table below. If the player wishes, they can produce 2 of the same type of warrior in one turn. If the player wishes, they can produce one warrior or no warriors at all and pass the turn.

Real human players must specify the x and y coordinates of the cell where they will place the warrior in the matrix after selecting the type of warrior from the menu. This process should continue until appropriate selections are made.

Once all players have completed the warrior selection and placement process, all warriors on the field will perform their attacks in the most appropriate way for the first player who placed them.

Players start the game with a Guardian placed randomly in one of the corners of the matrix. Newly placed warriors can only be placed adjacent to a previously placed warrior. The cell where the new warrior will be placed must either be empty or contain a different type of warrior than the player's own. If a new warrior is placed on top of a previously placed warrior, the old warrior is destroyed, and 80% of the resources used to create the old warrior are transferred to the treasury.

Users gain 10 resources per turn \+ the number of warriors in the world.

If a player has no warriors left in the world and passes 3 consecutive turns, they lose the game. If a player loses the game, all their warriors are removed from the world.

The player who remains in the world or controls 60% of the world wins the game.

Eğer başka bir çeviri ihtiyacınız olursa, memnuniyetle yardımcı olurum. Ne düşünüyorsunuz?
