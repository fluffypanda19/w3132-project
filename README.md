# w3132-project
# COMS W3132 Individual Project

## Author
Michael Wang
mw3665@columbia.edu

## Project Title
1v1 Fighter Pilot Game

## Project Description
This game is a 1v1 game where each player plays as a fighter jet that can move around 
the screen using wasd for player 1 and the arrow keys for player 2. Players must avoid 
projectiles that constantly rain down from the top of the screen while trying to shoot 
and kill each other. There will be features such as powerups, special projectiles/
environmental hazards that the players can interact with, etc.

This project does not aim to solve anything and is purely for entertainment purposes.
Furthermore, I've always been interested in game development so I would like to take
this opportunity to make my own game.

## Requirements, Features and User Stories
Rules:
1. Fly around the screen and shoot your opponent
2. Dodge bullets that rain down from the sky as well as enemy shots
3. Buffs will periodically drop from the sky with various effects
4. If you reach 0 health, you lose!
   
Player 1 Controls:
| Key | Action |
| ------------- | ------------- |
| w | up |
| a | left |
| s | down |
| d | right |
| Lshift | shoot |

Player 2 Controls:
| Key | Action |
| ------------- | ------------- |
| up arrow | up |
| left arrow | left |
| down arrow | down |
| right arrow | right |
| Rshift | shoot |

Buffs:
| Color | Effect |
| ------------- | ------------- |
| blue | freezing bullets - shoot bullets that slow the enemy on impact (lasts 5 seconds) |
| purple | speedy bullets -  your bullets travel faster (lasts 3 seconds) |
| pink | rapid fire -  attack cooldown is decreased (lasts 3 seconds) |
| red | speed -  your movement speed is increased (lasts 4 seconds) |
| brown | shield - negates next instance of damage taken, breaks upon taking damage (lasts 20 seconds) |
| geen | heal - restore 1 player health (cannot heal above max health) |

## Technical Specification
The pygame library as well as the built-in random module are required to run this 
game.

## Development Methodology
I dveloped my code in small chunks and tested the game in between said chunks before
moving onto the next one. For example, I will first ensure that basic player movement 
is working as intended before adding player attack functionality.

For testing, I manually tested all features of the game myself in order to make sure 
they are working in a way that is intuitive to the player as well as for balancing
the game to make sure features such as player speed, bullet velocity, buff durations, etc.
felt fair to play with and against.

## Potential Challenges and Roadblocks
This was my first time using the pygame library and as such I required some help with 
getting started. To help me get started, I did research online and found some resources
that gave me an overview on how to get started with pygame.

## Additional Resources
This youtube video tutorial https://www.youtube.com/watch?v=s5bd9KMSSW4 as well as
the pygame documentation website were instrumental in my success for this project.

The following assets were used to make this game:
- https://www.vectorstock.com/royalty-free-vector/8bit-pixel-graphic-blue-sky-background-with-clouds-vector-50920187
- https://thenounproject.com/icon/empty-pixel-heart-3907592/
- https://thenounproject.com/icon/shiny-pixel-heart-3907590/
- https://www.reddit.com/r/PixelArt/comments/i34exa/a_little_pixel_art_of_a_shield_i_just_did_in_32p/

## Conclusion and Future Work
Unfortunately due the the timeframe of this project (and my lack of experience with digital art),
this game is lacking many assets such as sprites for the planes and buffs. If I were to continue
this project I would definitely look into adding this in for a more polished look.

In terms of features, I would also like to add functionality for more than two players (maybe an
option for a 2v2 mode), more buffs, different kinds of hazards that players must avoid or can interact
with.

I would say this project was successful in accomplishing the goals I set out with when coming up with
this game and would love to do something similar in the future!
