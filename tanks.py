#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from player import Tank
from block import Platform
from pygame import *

WIN_WIDTH = 500
WIN_HIGHT = 500
DISPLAY = (WIN_WIDTH, WIN_HIGHT)
BACKGROUND_COLOR =  '#7FFF00'


PLATFORM_WIDTH = 50
PLATFORM_HEIGHT = 50
PLATFORM_COLOR = '#FF1493'

def main():
    tank = Tank(100,100)
    left = right = up = down = False
    entities = pygame.sprite.Group()
    platforms = []
    entities.add(tank)

    level  = ['**********',
              '*        *',
              '*   *    *',
              '*   *    *',
              '* *   *  *',
              '**     * *',
              '* *   *  *',
              '*  * *   *',
              '*        *',
              '**********',]
    timer = pygame.time.Clock()


    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Tanks")
    bg = Surface((WIN_WIDTH, WIN_HIGHT))

    bg.fill(Color(BACKGROUND_COLOR))

    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True

            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False


            if e.type == QUIT:
                raise SystemExit, "QUIT"

        screen.blit(bg, (0,0))
        x=y=0
        for row in level:
            for col in row:
                if col == "*":
                    pf = Platform(x,y)
                    entities.add(pf)
                    platforms.append(pf)
                x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT    #то же самое и с высотой
            x = 0

        tank.update(left, right, up, down, platforms)
        entities.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
