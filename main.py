import pygame, sys
from player import Player
from laser import Laser
import obstacle
from human import Human, Extra
from random import choice, randint


class Game:
    def __init__(self):
        #arcos
        player_spirit = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_spirit)

        #obstacle
        self.shape  = obstacle.shape
        self.block_size = 5
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 3
        self.obstacle_x_positions = [(num * (screen_width / self.obstacle_amount)) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(*self.obstacle_x_positions, x_start=screen_width/10, y_start=450)



        #human
        self.humans = pygame.sprite.Group()
        self.human_lasers = pygame.sprite.Group()
        self.human_setup(rows=5, cols=5)
        self.human_direction = 1

        #extra
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

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

    def human_setup(self, rows, cols, x_distance=120, y_distance=70,
                    x_offset=40, y_offset=65):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: human_sprite = Human("bald", x, y)
                elif 1<= row_index <= 2: human_sprite = Human("2", x, y)
                else: human_sprite = Human("1", x, y)
                self.humans.add(human_sprite)

    def human_position_checker(self):
        all_human = self.humans.sprites()
        for human in all_human:
            if human.rect.right >= screen_width:
                self.human_direction = -1
                self.human_move_down(0.4)
            elif human.rect.left <= 0:
                self.human_direction = 1
                self.human_move_down(0.4)

    def human_move_down(self, distnace):
        if self.humans:
            for human in self.humans.sprites():
                human.rect.y += distnace

    def human_shoot(self):
        if self.humans.sprites():
            random_human = choice(self.humans.sprites())
            laser_sprite = Laser(random_human.rect.center, speed=1
                                 , screen_height=screen_height)
            self.human_lasers.add(laser_sprite)


    def extra_human_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(["right", "left"]), screen_width))
            self.extra_spawn_time = randint(400, 800)


    def run(self):
        HUMANLASER = pygame.USEREVENT + 1
        pygame.time.set_timer(HUMANLASER, 800)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == HUMANLASER:
                    game.human_shoot()


            screen.fill((30, 30, 30))
            self.player.update()
            self.humans.update(self.human_direction)
            self.human_position_checker()
            #self.human_shoot()
            self.human_lasers.update()
            self.extra_human_timer()
            self.extra.update()
            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.blocks.draw(screen)
            self.humans.draw(screen)
            self.human_lasers.draw(screen)
            self.extra.draw(screen)

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

