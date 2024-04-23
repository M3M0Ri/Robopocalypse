import pygame, sys
from player import Player
from laser import Laser
import obstacle
from human import Human


class Game:
    def __init__(self):
        #arcos
        player_spirit = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_spirit)

        #obstacle
        self.shape  = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 3
        self.obstacle_x_positions = [(num * (screen_width / self.obstacle_amount)) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(*self.obstacle_x_positions, x_start=screen_width/15, y_start=480)



        #human
        self.humans = pygame.sprite.Group()
        self.human_setup(rows=6, cols=8)


    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (93, 63, 211), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacle(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def human_setup(self, rows, cols, x_distance=65, y_distance=50,
                    x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: human_sprite = Human("bald (1)", x, y)
                elif 1<= row_index <= 2: human_sprite = Human("2 (3)", x, y)
                else: human_sprite = Human("1 (2)", x, y)
                self.humans.add(human_sprite)



    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill((30, 30, 30))
            self.player.update()
            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.blocks.draw(screen)
            self.humans.draw(screen)

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    game = Game()
    game.run()
