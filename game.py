import math

import pyglet


class InputManager:
    TOGGLE_PAUSE, MOVE_LEFT, MOVE_RIGHT, START_BALL = range(4)

    def __init__(self):
        self.action = None
        self.down_left = False
        self.down_right = False

    def key_press(self, symbol, modifiers):
        from pyglet.window.key import (
            MOTION_LEFT, MOTION_RIGHT, SPACE, ENTER
        )
        if symbol == SPACE:
            self.action = InputManager.START_BALL
        elif symbol == ENTER:
            self.action = InputManager.TOGGLE_PAUSE
        elif symbol == MOTION_LEFT:
            self.down_left = True
        elif symbol == MOTION_RIGHT:
            self.down_right = True

    def key_release(self, symbol, modifiers):
        from pyglet.window.key import (
            MOTION_LEFT, MOTION_RIGHT
        )
        if symbol == MOTION_LEFT:
            self.down_left = False
        elif symbol == MOTION_RIGHT:
            self.down_right = False

    def consume(self):
        action = None
        if self.action is None:
            if self.down_right and self.down_left:
                action = None
            elif self.down_left:
                action = InputManager.MOVE_LEFT
            elif self.down_right:
                action = InputManager.MOVE_RIGHT
        else:
            action = self.action
            self.action = None
        return action


class Game:
    LEFT, TOP, RIGHT, BOTTOM = range(4)

    def __init__(self, window, im):
        self.window = window
        self.input = im
        self.block_list = []
        self.batch = pyglet.graphics.Batch()
        self.ball = None
        self.paddle = None
        self.ball_angle = 0
        self.ball_speed = 5
        self.ball_dx = 0
        self.ball_dy = 0
        self.lost = False

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
            ball_image, 150, 150, batch=self.batch
        )
        self.set_ball_angle()

    def create_paddle(self, paddle_image):
        dx = self.window.width / 2 - paddle_image.width / 2
        dy = self.window.height / 8
        self.paddle = pyglet.sprite.Sprite(
            paddle_image, dx, dy, batch=self.batch
        )

    def draw(self):
        self.batch.draw()

    def update(self):
        if self.lost:
            pass
        else:
            self.move_ball()
            command = self.input.consume()
            if command == InputManager.MOVE_LEFT:
                self.paddle.x -= 5
                if self.paddle.x < 0:
                    self.paddle.x = 0
            elif command == InputManager.MOVE_RIGHT:
                self.paddle.x += 5
                if self.paddle.x + self.paddle.width > self.window.width:
                    self.paddle.x = self.window.width - self.paddle.width

    def set_ball_angle(self, angle=45):
        self.ball_angle = math.radians(angle)
        self.ball_dx = math.cos(self.ball_angle) * self.ball_speed
        self.ball_dy = math.sin(self.ball_angle) * self.ball_speed

    def flip_ball_vector(self, is_x=False):
        if is_x:
            self.ball_dx *= -1
        else:
            self.ball_dy *= -1

    def ball_collided(self, target):
        # ball's left, top, right, bottom
        bl = self.ball.x
        bt = self.ball.y
        br = bl + self.ball.width
        bb = bt - self.ball.height
        # target's left, top, right, bottom
        tl = target.x
        tt = target.y
        tr = tl + target.width
        tb = tt - target.height

        # check horizontal range
        if tl <= br + self.ball_dx and bl + self.ball_dx <= tr:
            # check top
            if bt <= tb <= bt + self.ball_dy:
                return Game.TOP
            # check bottom
            elif bb + self.ball_dy <= tt <= bb:
                return Game.BOTTOM

    def move_ball(self):
        if self.ball.x + self.ball.width + self.ball_dx >= self.window.width:
            self.flip_ball_vector(True)
            self.ball.x = self.window.width - self.ball.width

        if self.ball.x + self.ball_dx <= 0:
            self.flip_ball_vector(True)
            self.ball.x = 0

        if self.ball.y + self.ball_dy >= self.window.height:
            self.flip_ball_vector()
            self.ball.y = self.window.height

        paddle_collide = self.ball_collided(self.paddle)
        if paddle_collide == Game.BOTTOM:
            cx = self.ball.x + self.ball.width / 2
            paddle_part = [self.paddle.x + self.paddle.width * p / 5 for p in
                           range(0, 6)]
            base_angle = round(
                math.degrees(math.acos(self.ball_dy / math.sqrt(
                    self.ball_dx ** 2 + self.ball_dy ** 2))))
            if self.ball_dy < 0:
                base_angle = 360 - base_angle
            if self.ball_dx < 0:
                base_angle += 90
            if paddle_part[0] <= cx < paddle_part[1]:
                self.set_ball_angle(base_angle + 180 + 10)
            elif paddle_part[1] <= cx < paddle_part[2]:
                self.set_ball_angle(base_angle + 180 + 5)
            elif paddle_part[2] <= cx < paddle_part[3]:
                self.flip_ball_vector()
            elif paddle_part[3] <= cx < paddle_part[4]:
                self.set_ball_angle(base_angle + 180 - 5)
            elif paddle_part[4] <= cx < paddle_part[5]:
                self.set_ball_angle(base_angle + 180 - 10)

        self.ball.x += self.ball_dx
        self.ball.y += self.ball_dy
