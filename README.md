## :space_invader: About

This code uses the Pygame library to create a fireworks display. 

It starts by initializing Pygame and setting up the screen with a width and height of 800 and 600 pixels. The caption of the window is set to "Fogos de Artifício", which means "Fireworks" in Portuguese.

Next, some color variables are defined. 

Then, there are two classes defined: 
1. The Particle class represents a particle of the explosion. It has properties such as x and y coordinates, color, radius, angle, speed, explode_height, max_lifetime, and lifetime. It also has methods to move and draw the particle. 
2. The Rocket class represents a rocket. It has properties such as x and y coordinates, color, speed, exploded flag, particles list, and explode_height. It has methods to move, draw, and explode the rocket. 

After defining the classes, a list called rockets is created.

The code then enters a while loop, which runs until the game is exited. In the loop, it checks for any quit events from the user. 

Inside the loop, new rockets are randomly created and added to the rockets list. 

The screen is filled with black color. 

For each rocket in the rockets list, the rocket is moved and drawn. 

Any rockets that have either exploded completely or gone off the screen are removed from the rockets list. 

The screen is updated and the clock is ticked at a rate of 30 frames per second.

## :wrench: Requirements

The following Python libraries are required:

- pygame
- sys
- random
- math


## :runner:  Usage

, you would run the code in the terminal by typing the command:

python .\fireworks-pygame.py

## :raising_hand: Contribution

All contributions are welcome! Please open an issue or submit a pull request.

