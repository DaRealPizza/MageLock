import pygame, sys, socket, random, pickle

# constants
WINDOW_SIZE = (800, 600)
FPS = 60
TILE_SIZE = 40

serverip = input("Server ip: ")
serverport = 40183
clientip = socket.gethostbyname(socket.gethostname())
clientport = random.randint(10000, 65500)

# pygame initialization
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Magelock")
clock = pygame.time.Clock()

# mutable variables
enemies = []

stage_hitbox = pygame.Rect(80, 440, TILE_SIZE * 16, TILE_SIZE * 2)

hitboxes = [stage_hitbox,pygame.Rect(80, 280, TILE_SIZE * 4, TILE_SIZE),pygame.Rect(600, 400, TILE_SIZE * 4, TILE_SIZE)]

# images
mage = pygame.image.load("assets/characters/mage.png").convert_alpha()
mage = pygame.transform.scale(mage, (TILE_SIZE * 1, TILE_SIZE * 1))

# class image dict
classimg = {
    "mage" : mage
}

# player class
class Player(pygame.sprite.Sprite):
    def __init__(self, cls, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        #fetches image from class dict
        self.image = classimg[cls]
        self.imageleft = self.image
        self.imageright = pygame.transform.flip(self.image, True, False)
        self.animationstate = "left"

        # hitbox rect
        self.rect = pygame.Rect(posx, posy, TILE_SIZE, TILE_SIZE)

        # physics variables
        self.gravity = 1
        self.speed = 7
        self.jumpvel = 20
        self.yvel = 0
        self.xvel = 0
        self.isgrounded = False


    def update(self):
        # checks for input and puts it in a list
        intent = self.inputhandler()

        # moves player horizontally
        self.xvel = intent[0] * self.speed
        self.rect.x += self.xvel

        # checks for horizontal collision
        for i in hitboxes:
            if self.rect.colliderect(i):
                if self.xvel > 0:
                    self.rect.right = i.left
                if self.xvel < 0:
                    self.rect.left = i.right

        # moves player vertically
        self.yvel += self.gravity
        if intent[1] == 1:
            self.yvel -= self.jumpvel
            self.isgrounded = False
        self.rect.y += self.yvel

        # checks for vertical collision
        for i in hitboxes:
            if self.rect.colliderect(i):
                if self.yvel > 0:
                    self.rect.bottom = i.top
                    self.yvel = 0
                    self.isgrounded = True
                if self.yvel < 0:
                    self.rect.top = i.bottom
                    self.yvel = 0

        # makes sure player cant jump when you fall off a platform
        if self.yvel > 0:
            self.isgrounded = False

        if self.rect.y > WINDOW_SIZE[1] + 100:
            self.rect.x, self.rect.y = 380, 280
            self.xvel = 0
            self.yvel = 0

        # draws player
        if intent[0] > 0:
            self.image = self.imageright
            self.animationstate = "right"
        if intent[0] < 0:
            self.image = self.imageleft
            self.animationstate = "left"

        window.blit(self.image, (self.rect.x, self.rect.y))
        
            

    # checks for input
    def inputhandler(self):
        intent = [0,0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            intent[0] = -1
        if keys[pygame.K_RIGHT]:
            intent[0] = 1

        if keys[pygame.K_UP] and self.isgrounded: 
            self.isgrounded = False
            intent[1] = 1

        return intent

# class for player packets
class Packet:
    def __init__(self, x, y, cls, address, animationstate):
        self.x = x
        self.y = y
        self.cls = cls
        self.address = address
        self.animationstate = animationstate

# draws the enemies received from server
def drawEnemy(enemy):
    image = classimg[enemy.cls]
    x = enemy.x
    y = enemy.y
    imageleft = image
    imageright = pygame.transform.flip(image, True, False)
    if enemy.animationstate == "left":
        image = imageleft
    if enemy.animationstate == "right":
        image = imageright

    window.blit(image, (x, y))


# creating player (temp)
plr = Player("mage", 380, 280)


# joining server
con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

con.sendto(pickle.dumps("HEADER:JOIN"), (serverip, serverport))

# fetches room to check connection
con.sendto(pickle.dumps("HEADER:FETCHROOM"), (serverip, serverport))
try:
    data, addr = con.recvfrom(1024)
except:
    print(f"failed to connect to {serverip}:{serverport}")
    sys.exit()

# leave the server when game crashes
def crashhandler(type, value, tb):
    con.sendto(pickle.dumps("HEADER:CRASH"), (serverip, serverport))
    con.close()

sys.excepthook = crashhandler

# main function
def main():
    while True:
        global enemies

        # global events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                con.sendto(pickle.dumps("HEADER:LEAVE"), (serverip, serverport))
                con.close()
                pygame.quit()
                sys.exit()

        # draws stage (temp)
        for i in hitboxes:
            pygame.draw.rect(window, (69, 124, 96), i)

        # updates player
        plr.update()

        # sends player to server
        pack = Packet(plr.rect.x, plr.rect.y, "mage", (clientip, clientport), plr.animationstate)
        con.sendto(pickle.dumps(pack), (serverip, serverport))

        # receives other players' packets
        data, addr = con.recvfrom(1024)
        enemies = pickle.loads(data)

        # draw enemies received from server
        for i in enemies:
            if i.address == (clientip, clientport):
                continue
            drawEnemy(i)

        # pygame updates
        pygame.display.flip()
        window.fill((133, 167, 182))
        clock.tick(FPS)


if __name__ == "__main__":
    main()
