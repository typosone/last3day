import pyglet


class Game:
    def __init__(self):
        self.block_list = []

    def create_blocks(self, block_image):
        for y in range(6):
            for x in range(11):
                self.block_list.append(
                    Block(x, y, block_image)
                )

    def draw(self):
        for block in self.block_list:
            block.draw()

    def update(self):
        pass


class Block:
    BLOCK_WIDTH = 30
    BLOCK_HEIGHT = 20
    X_MARGIN = 35
    Y_MARGIN = 450

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self):
        x = self.x * self.BLOCK_WIDTH + self.X_MARGIN
        y = self.y * self.BLOCK_HEIGHT + self.Y_MARGIN
        self.image.blit(x, y)
