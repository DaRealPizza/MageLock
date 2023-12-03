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

# screen coords to world coords
def getworldcoords(x, y):
    return x / GRID_X, y / GRID_Y

# mutable variables
stage_hitbox = pygame.Rect(getcoords(2, 11)[0], getcoords(2, 11)[1], TILE_SIZE * 16, TILE_SIZE * 2)

hitboxes = [stage_hitbox,pygame.Rect(getcoords(2, 7)[0], getcoords(2, 7)[1], TILE_SIZE * 4, TILE_SIZE),pygame.Rect(getcoords(15, 10)[0], getcoords(15, 10)[1], TILE_SIZE * 4, TILE_SIZE)]

showhitboxes = False

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
        self.imageleft = self.image
        self.imageright = pygame.transform.flip(self.image, True, False)
        self.tempx = 0

        self.rect = pygame.Rect(getcoords(posx, posy)[0], getcoords(posx, posy)[1], TILE_SIZE, TILE_SIZE)

        self.gravity = 2
        self.speed = 15
        self.jumpvel = 40

        self.isgrounded = False

        self.yvel = 0
        self.xvel = 0

    # draws player
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        if showhitboxes:
            pygame.draw.rect(window, (0,255,0), self.rect)

    def update(self):
        # checks for input and puts it in a list
        intent = self.inputhandler()

        # checks if we can move the player horizontally
        self.yvel += self.gravity / 100

        collideh = self.horizontal_collision(intent)

        #check vertical collision
        self.vertical_collision()

        if intent[1] == 1:
            self.yvel -= self.jumpvel / 100
            self.isgrounded = False
        

        self.rect.y += getcoords(0,self.yvel)[1]
        if collideh:
            self.rect.x += getcoords(self.xvel,0)[0]

        self.xvel = 0
    
    def vertical_collision(self):
        for i in hitboxes:
            if self.rect.colliderect(i):
                if self.yvel > 0:
                    self.rect.bottom = i.top + 2
                    self.isgrounded = True
                if self.yvel < 0:
                    self.rect.top = i.bottom
                
                self.yvel = 0

    def horizontal_collision(self, intent):
        if intent[0] == -1:
            self.xvel = -self.speed / 100
        if intent[0] == 1:
            self.xvel = self.speed / 100

        self.rect.x += getcoords(self.xvel,0)[0]
        for i in hitboxes:
            if self.rect.colliderect(i):
                self.rect.x -= getcoords(self.xvel,0)[0]
                self.xvel = 0
                return False
            
        self.rect.x -= getcoords(self.xvel,0)[0]
        self.xvel = 0
        return True
        
            


    def inputhandler(self):
        intent = [0,0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            intent[0] = -1
        if keys[pygame.K_RIGHT]:
            intent[0] = 1

        if keys[pygame.K_UP] and self.isgrounded is True: 
            self.isgrounded = False
            intent[1] = 1

        return intent
    

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    global showhitboxes
                    showhitboxes = not showhitboxes
        
        plr.update()
        
        # drawing stage (temp)
        for x in range(2, 18):
            pygame.draw.rect(window, (111,84,76), pygame.Rect(getcoords(x, 12)[0], getcoords(x, 12)[1], TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(window, (69,124,96), pygame.Rect(getcoords(x, 11)[0], getcoords(x, 11)[1], TILE_SIZE, TILE_SIZE))

        if showhitboxes:
            for i in hitboxes:
                pygame.draw.rect(window, (0,0,255), i)

        # drawing sprites
        plr.draw()

        # pygame updates
        pygame.display.flip()
        window.fill((100, 100, 200))
        clock.tick(FPS)


if __name__ == "__main__":
    main()
