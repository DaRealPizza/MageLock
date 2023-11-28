import pygame, sys

WINDOW_SIZE = (800, 600)
FPS = 60

# grid is 40 by 30
TILE_SIZE = 20
GRID_X = WINDOW_SIZE[0] / 40
GRID_Y = WINDOW_SIZE[1] / 30

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Magelock")
clock = pygame.time.Clock()

def getcoords(x, y):
    return x * GRID_X, y * GRID_Y

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        for x in range(9, 30):
            pygame.draw.rect(window, (111,84,76), pygame.Rect(getcoords(x, 20)[0], getcoords(x, 20)[1], TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(window, (69,124,96), pygame.Rect(getcoords(x, 19)[0], getcoords(x, 19)[1], TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        window.fill((100, 100, 200))
        clock.tick(FPS)


if __name__ == "__main__":
    main()
