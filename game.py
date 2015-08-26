import math

import pyglet


class Game:
    def __init__(self, window):
        self.window = window
        self.block_list = []
        self.batch = pyglet.graphics.Batch()
        self.ball = None
        self.ball_angle = math.radians(45)
        self.ball_speed = 5

    def create_blocks(self, block_image):
        for y in range(6):
            for x in range(11):
                self.block_list.append(
                    pyglet.sprite.Sprite(
                        block_image, x * 30 + 35, y * 20 + 450,
                        batch=self.batch
                    )
                )

    def create_ball(self, ball_image):
        self.ball = pyglet.sprite.Sprite(
            ball_image, 150, 100, batch=self.batch
        )

    def draw(self):
        self.batch.draw()

    def update(self):
        self.move_ball()

    def change_ball_angle(self, positive=True):
        if positive:
            self.ball_angle += math.radians(90)
        else:
            self.ball_angle -= math.radians(90)

    def move_ball(self):
        x = math.cos(self.ball_angle) * self.ball_speed
        y = math.sin(self.ball_angle) * self.ball_speed

        if self.ball.x + x >= self.window.width:
            x = self.window.width - (self.ball.x + x)
            self.change_ball_angle(y > 0)

        if self.ball.x + x <= 0:
            x = abs(self.ball.x + x)
            self.change_ball_angle(y < 0)

        if self.ball.y + y >= self.window.height:
            y = self.window.height - (self.ball.y + y)
            self.change_ball_angle(x < 0)

        self.ball.x += x
        self.ball.y += y
