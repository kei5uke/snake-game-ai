# snake-game-ai
I created snake game and trained neural network to beat the game because why not.
## Base Game (Pygame)
I used the Pygame library for creating the base snake game.  
Snake at the start and apple(food) at each moment will be placed on the map randomly. 
## Neural Network
To make snake smart, we need to give knowledge to it.  
Considering the main tasks of the game are survive and earn score, the best way to make the snake smart is giving which direction is safe and close to the food.  

### Features as an input
I decided to give these features below for the NN input.  
Output (label) will be collected after the snake moves 1 step every time.
#### Input
- Blocked direction [ UP, RIGHT, DOWN, LEFT ] True : 1 / False : 0 
- Distance of the food 
- Distance of walls
- Normalized angle between snake's movement direction and direction to an apple
- Suggested direction [ UP, RIGHT, DOWN, LEFT ] True : 1 / False : 0   

#### Output
- 1 - Snake survived and moved to the right direction (direction to the food)
- 0 - Snake survived but the direction was wrong
- -1 - Snake died   

### NN Architecture
2 hidden layers of Relus, and linear layer as an output layer.

## Experiment
I let the snake moves randomly and see how they make difference in their movement.  
Let's see how snake evolves in every generation.

### Data collection and result
As a result, I got 13 million steps of data from 100K generation of snakes.  
Here's the average score of every generation.  
![avg_score](https://user-images.githubusercontent.com/33390452/133888103-599672c0-9294-4db7-9c42-0fdeeab66f0d.png)  
As you can see, the average score goes higher as the amount of data increases. Especially from the gen 5k to 400k.  
Above gen 600k decrease avg score so probably they are overfitting and need some parameter tuning.
#### Gen 5000  
![gen5k](https://user-images.githubusercontent.com/33390452/133888073-3db00647-0bf9-4c23-89f9-f513af90af8a.gif)  
#### Gen 10000  
![10k](https://user-images.githubusercontent.com/33390452/133888072-22112dc2-d117-4485-9373-64d925ea86b1.gif)  
#### Gen 100000    
![100k](https://user-images.githubusercontent.com/33390452/133888071-a7059607-eb49-4796-b9f3-27bf780d0acf.gif)
#### Gen 200000  
![200k](https://user-images.githubusercontent.com/33390452/133888070-1da04538-fd1a-4f1c-910c-7842bd0a28ad.gif)  
#### Gen 400000  
![400k](https://user-images.githubusercontent.com/33390452/133888069-3e05f0d2-6774-4c16-8316-4a0be59504b5.gif)  
#### Gen 600000  
![600k](https://user-images.githubusercontent.com/33390452/133888067-947e5c6e-225a-4c98-88a0-924e1492d4b7.gif)  
#### Gen 800000  
![800k](https://user-images.githubusercontent.com/33390452/133888065-b1436262-67e7-46e7-9714-8a75d155cd67.gif)  
Movement of snakes appears to be gradually becoming more linear.

