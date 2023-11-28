import pygame, sys

WINDOW_SIZE = (800, 600)
FPS = 60

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Magelock")
clock = pygame.time.Clock()

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        window.fill((100, 100, 200))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
