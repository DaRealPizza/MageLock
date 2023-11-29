import pygame, sys

# constants
WINDOW_SIZE = (800, 600)
FPS = 60

# - grid is 40 by 30
TILE_SIZE = 40
GRID_X = WINDOW_SIZE[0] / 20
GRID_Y = WINDOW_SIZE[1] / 15

# pygame initialization
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Magelock")
clock = pygame.time.Clock()

# world coords to screen coords
def getcoords(x, y):
    return x * GRID_X, y * GRID_Y

# mutable variables
stage_hitbox = pygame.Rect(getcoords(2, 11)[0], getcoords(2, 11)[1], TILE_SIZE * 16, TILE_SIZE * 2)

mage = pygame.image.load("assets/characters/mage.png").convert_alpha()
mage = pygame.transform.scale(mage, (TILE_SIZE * 1, TILE_SIZE * 1))

classes = {
    "mage" : mage
}

# player class
class Player(pygame.sprite.Sprite):
    def __init__(self, cls, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = classes[cls]
        self.x = posx
        self.y = posy

        self.rect = self.image.get_rect()

    def draw(self):
        window.blit(self.image, (getcoords(self.x, self.y)))

    def update(self):
        pass

# creating player (temp)
plr = Player("mage", 10, 7)


# main function
def main():
    while True:
        
        # global events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        plr.update()
        
        # drawing stage (temp)
        for x in range(2, 18):
            pygame.draw.rect(window, (111,84,76), pygame.Rect(getcoords(x, 12)[0], getcoords(x, 12)[1], TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(window, (69,124,96), pygame.Rect(getcoords(x, 11)[0], getcoords(x, 11)[1], TILE_SIZE, TILE_SIZE))

        pygame.draw.rect(window, (255,0,0), stage_hitbox)

        # drawing sprites
        plr.draw()

        # pygame updates
        pygame.display.flip()
        window.fill((100, 100, 200))
        clock.tick(FPS)


if __name__ == "__main__":
    main()
