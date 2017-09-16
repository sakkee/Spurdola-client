# Spurdola (client)

## About
Spurdola is a (unfinished) Pyglet-based multiplayer RPG game that utilizes twisted. The Python version used is 2.7. 

The client version includes the client versions of game, updater, mapcreator and npccreator.

The coding style is not pretty and is pretty much undocumented and uncommented. The client code ought to be rewritten. 

This repository is about the client-side of the game. The server-side has its own repository [own repository](https://github.com/sakkee/Spurdola-servers).

## Installation
### Version and modules
The Python version used is 2.7. (Atleast) the following libraries need to be installed:
- twisted
- pygame
- numpy
- py2exe
- PIL
- ConfigParser

### Configuration
constants.py:
- GAME_VERSION should be up to date and the same as the login server's
- GAME_IP should be updated to correspond the IP address or domain address of the loginserver

gamelogic.py:
- GAME_IP should be updated to correspond the IP address or domain address of the loginserver

### Running
```
python goldenes.py
```
