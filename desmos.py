import pygame
from graphwar2 import *

pygame.init()

width = 1274
height = 763
screen = pygame.display.set_mode((width, height))

running = True
x_points, points = function_generator((0, 0), (10, 10), type='double_abs')
x_points = x_points * tile_to_pixel
points = -points * tile_to_pixel
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.line(screen, (0, 0, 0), (width/2, 0), (width/2, height), 2)
    pygame.draw.line(screen, (0, 0, 0), (0, height/2), (width, height/2), 2)
    #draw the points buddy
    for i in range(len(x_points)-1):
        x1 = width / 2 + x_points[i]
        y1 = height / 2 - points[i]
        x2 = width / 2 + x_points[i + 1]
        y2 = height / 2 - points[i + 1]
        pygame.draw.line(screen, (255, 0, 0), (x1, y1), (x2, y2), 2)

    pygame.display.flip()