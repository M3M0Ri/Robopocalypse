import pygame, sys
from player import Player
from laser import Laser
import obstacle
from human import Human, Extra
from random import choice, randint


class Game:
    def __init__(self):
        #arcos
        player_spirit = Player((screen_width / 2, screen_height), screen_width, 6)
        self.player = pygame.sprite.GroupSingle(player_spirit)

        #health and score setup
        self.lives = 4
        self.live_surf = pygame.image.load("graphics/arcos3.png").convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 70)
        self.score = 0
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)

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

        #music
        music = pygame.mixer.Sound("music/music.mp3")
        music.set_volume(0.2)
        music.play(loops= -1)
        self.laser_sound = pygame.mixer.Sound("music/laser.mp3")
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound("music/explosion.wav")
        self.explosion_sound.set_volume(0.3)

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
                self.human_move_down(0.8)
            elif human.rect.left <= 0:
                self.human_direction = 1
                self.human_move_down(0.8)

    def human_move_down(self, distnace):
        if self.humans:
            for human in self.humans.sprites():
                human.rect.y += distnace

    def human_shoot(self):
        if self.humans.sprites():
            random_human = choice(self.humans.sprites())
            laser_sprite = Laser(random_human.rect.center, speed=0.5
                                 , screen_height=screen_height)
            self.human_lasers.add(laser_sprite)


    def extra_human_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(["right", "left"]), screen_width))
            self.extra_spawn_time = randint(400, 800)

    def collision_checks(self):
        #player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                #obstical collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()


                # human collisions
                humans_hit = pygame.sprite.spritecollide(laser, self.humans, True)
                if humans_hit:
                    for human in humans_hit:
                        self.score += human.value
                    laser.kill()
                    self.explosion_sound.play()

                # extra collisions
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()


        #human laser
        if self.human_lasers:
            for laser in self.human_lasers:
                # obstical collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()


                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        #humans
        if self.humans:
            for human in self.humans:
                pygame.sprite.spritecollide(human, self.blocks, True)

                if pygame.sprite.spritecollide(human, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'yellow')
        score_rect = score_surf.get_rect(topleft=(10, -10))
        screen.blit(score_surf, score_rect)

    def victory_message(self):
        if not self.humans.sprites():
            victory_surf = self.font.render('YOU WON !!', False, 'green')
            victory_rect = victory_surf.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)

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
            self.collision_checks()

            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.blocks.draw(screen)
            self.humans.draw(screen)
            self.human_lasers.draw(screen)
            self.extra.draw(screen)
            self.display_lives()
            self.display_score()
            self.victory_message()

            pygame.display.flip()
            clock.tick(60)


class CRT:
    def __init__(self):
        self.tv = pygame.image.load("graphics/tv.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        screen.blit(self.tv, (0, 0))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)



if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    game = Game()
    crt = CRT()
    game.run()
    crt.draw()


