import sys, pygame
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print(BASE_DIR)

pygame.init()

screen = pygame.display.set_mode((600, 480))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((255, 255, 255))
    #left, top, width, height
    pygame.draw.rect(screen, [255, 0, 0], (10, 10, 214, 43))
    #center, radius
    pygame.draw.circle(screen, [0, 255, 0], (300, 300), 100)
    #[point,point,...]
    pygame.draw.polygon(screen, [0, 0, 255], [(20, 30), (55, 78), (49, 120)])
    pygame.display.flip()
