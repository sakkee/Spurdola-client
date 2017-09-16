import pyglet
pyglet.lib.load_library('avbin')
pyglet.have_avbin=True
music = pyglet.media.load('pokemon.mp3')
player = pyglet.media.Player()
player.queue(music)
player.play()

pyglet.app.run()