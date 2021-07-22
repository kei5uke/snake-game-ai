# snake-game-ai
I created snake game and trained neural network to beat the game because why not :P 
## pygame
I used pygame library for creating the base snake game. Snake at the start and apple(food) at each moment will be placed on the map. 
## Neural Network
To make snake smart, we need to give knowledge to it. Considering the main tasks of the game are survive and earn score, the snake should know which direction is safe and close to the food. 
Soo I decide to give these features below for the neural network.
### Input
- Blocked direction [ UP, RIGHT, DOWN, LEFT ] 1 - if True, 0 - False 
- Normalized angle between snake's movement direction and direction to an apple
- Suggested direciton [ UP, RIGHT, DOWN, LEFT ] 1 - if True, 0 - False  
### Output
- 1 - Snake survived and moved to the right direction
- 0 - Snake survived but the direction was wrong
- -1 - Snake died  
### Architecture
Descent number of Relu in the hidden layer.
Ouput layer is linear.
