import sys, pygame
import svgparser
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print(BASE_DIR)

pygame.init()


class Map:
    def __init__(self, mapData):
        self.finished = False
        self.wall = pygame.image.load(os.path.join(BASE_DIR, "data/wall24x24.png"))
        self.out = pygame.image.load(os.path.join(BASE_DIR, 'data/out24x24.png'))
        self.you = pygame.image.load(os.path.join(BASE_DIR, 'data/you24x24.png'))
        self.map = []
        for l in mapData.split('\n'):
            if not l:
                continue
            self.map.append(list(l))

        self.rows = len(self.map[0])
        self.cols = len(self.map)
        self.row, self.col = 0 ,0
        for i, r in enumerate(self.map):
            for j, c in enumerate(r):
                if 'S' == c:
                    self.row, self.col = j, i

    def render(self, screen):

        for i, r in enumerate(self.map):
            for j, c in enumerate(r):
                ballrect = self.wall.get_rect()
                ballrect = ballrect.move((j * 24, i * 24))
                if '#' == c:
                    screen.blit(self.wall, ballrect)
                if 'X' == c:
                    screen.blit(self.out, ballrect)
        ballrect = self.wall.get_rect()
        ballrect = ballrect.move((self.row*24, self.col*24))
        screen.blit(self.you, ballrect)

        if 'X' == self.map[self.col][self.row]:
            print('GOOD')
            self.finished = True

    def moveUp(self):
        self.move(0, -1)
    def moveDown(self):
        self.move(0, 1)
    def moveLeft(self):
        self.move(-1, 0)
    def moveRight(self):
        self.move(1, 0)

    def move(self, rowOffset, colOffset):
        newRow = self.row + rowOffset
        newCol = self.col + colOffset
        if(newRow < 0 or newRow >= self.rows):
            return
        if(newCol <0 or newCol >= self.cols):
            return
        if '#' == self.map[newCol][newRow]:
            return
        self.row = newRow
        self.col = newCol



maps = [os.path.join(BASE_DIR, 'data/%s.svg'%i) for i in range(1, 7)]

mapData = svgparser.parsesvg(maps.pop())
map = Map(mapData)

screen = pygame.display.set_mode((map.rows * 24, map.cols * 24))


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                map.moveUp()
            elif event.key == pygame.K_LEFT:
                map.moveLeft()
            elif event.key == pygame.K_RIGHT:
                map.moveRight()
            elif event.key == pygame.K_DOWN:
                map.moveDown()

    screen.fill((255, 255, 255))
    map.render(screen)
    pygame.display.flip()

    if map.finished:
        mapData = svgparser.parsesvg(maps.pop())
        map = Map(mapData)


