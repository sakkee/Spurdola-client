import pyglet
import global_vars as g
import engine

if __name__ == '__main__':
    g.gameEngine = engine.Engine()
    g.gameEngine.init()