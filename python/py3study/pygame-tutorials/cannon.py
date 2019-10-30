"""
作为初始代码，目标是有的一个固定大小的球，给定一个初识速度，和一个固定阻力，演示球运动的过程。每一个循环的时间与现实时间一致。
从最初代码开始演示如何一步步完善代码最终完成功能的过程。
"""
import sys, pygame
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print(BASE_DIR)

pygame.init()

screen = pygame.display.set_mode((600, 480))

ball_center = (30, 30)
ball_color = [0, 255, 0]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((255, 255, 255))
    # 在前进方向上移动一步
    pygame.draw.circle(screen, ball_color, ball_center, 10)
    pygame.display.flip()
