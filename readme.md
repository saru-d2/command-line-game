# brick breaker
### dass assignment 3
asses 2 AND 3

## DASS assignment 2

uses OOPS :O

instructions to run:

```python3
    python3 main.py
```

ensure that colorama and numpy are installed


Controls: space to launch, a to move left, d to move rightm p to skip, l to activate lasers!!

OOPS concepts:

- inheritence: Standard_brick, exploding_brick and unbreakable brick all inherit parent class parent_brick
- Polymorphism: the show function of each class, hit for the different kinds of bricks amongst others
- Encapsulatoion: all functionality done with classes and objects
- abstraction: class functions hide the inner workings of each function appropriately behind well descriptive function names

changes since ass2: (see branch ass2 for clarity)
- added levels: before they were random, now, predetermined
- added powerup physics, the powerups follow are parabolic path
- bricks lower every 10 seconds
- theres a boss (a ufo)
- added powerup shooting paddle: gives the paddle 2 lazers
- added powerup fireball: gives the ball a blast radius
- added a sound effect for the ball

