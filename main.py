import pygame, sys, socket, random, pickle

# constants
WINDOW_SIZE = (800, 600)
FPS = 60
TILE_SIZE = 40

# pygame initialization
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Magelock")
clock = pygame.time.Clock()

# mutable variables
ip = "127.0.0.1"
serverport = 40183
clientport = random.randint(10000, 65500)

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

        # draws player
        window.blit(self.image, (self.rect.x, self.rect.y))
            

    # checks for input
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
    
class Packet:
    def __init__(self, x, y, cls, address):
        self.x = x
        self.y = y
        self.cls = cls
        self.address = address


# creating player (temp)
plr = Player("mage", 380, 280)


# joining server
con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
con.bind((ip, clientport))

con.sendto(pickle.dumps("HEADER:JOIN"), (ip, serverport))

con.sendto(pickle.dumps("HEADER:FETCHROOM"), (ip, serverport))
try:
    data, addr = con.recvfrom(1024)
except:
    print(f"failed to connect to {ip}:{serverport}")
    sys.exit()

room = pickle.loads(data)
print(room)

# main function
def main():
    while True:
        global enemies

        # global events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                con.sendto(pickle.dumps("HEADER:LEAVE"), (ip, serverport))
                con.close()
                pygame.quit()
                sys.exit()

        # draws stage (temp)
        for i in hitboxes:
            pygame.draw.rect(window, (0,0,255), i)

        # updates player
        plr.update()

        # sends player to server
        pack = Packet(plr.rect.x, plr.rect.y, "mage", (ip, clientport))
        con.sendto(pickle.dumps(pack), (ip, serverport))

        data, addr = con.recvfrom(1024)
        enemies = pickle.loads(data)

        for i in enemies:
            print(i.address)

        # pygame updates
        pygame.display.flip()
        window.fill((100, 100, 200))
        clock.tick(FPS)


if __name__ == "__main__":
    main()
