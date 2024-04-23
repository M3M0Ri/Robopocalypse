import pygame, sys
from player import Player
from laser import Laser


class Game:
    def __init__(self):
        player_spirit = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_spirit)

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
