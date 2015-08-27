import pyglet

import game

WIDTH = 400
HEIGHT = 600

if __name__ == '__main__':
    block_image = pyglet.resource.image('block.png')
    ball_image = pyglet.resource.image('ball.png')
    paddle_image = pyglet.resource.image('paddle.png')
    window = pyglet.window.Window(WIDTH, HEIGHT)
    window.set_vsync(False)
    i = game.InputManager()
    g = game.Game(window, i)
    g.create_blocks(block_image)
    g.create_ball(ball_image)
    g.create_paddle(paddle_image)


    @window.event
    def on_draw():
        window.clear()
        g.draw()


    @window.event
    def on_key_press(symbol, modifiers):
        i.key_press(symbol, modifiers)


    @window.event
    def on_key_release(symbol, modifiers):
        i.key_release(symbol, modifiers)

    def update(dt):
        g.update()


    pyglet.clock.schedule_interval(update, 1 / 60.0)
    pyglet.app.run()
