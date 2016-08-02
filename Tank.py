#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, pygame
from pygame import *
from Block import *
from Bullet import *

class Tank(sprite.Sprite):
    def __init__(self,topleft):
        sprite.Sprite.__init__(self)
        self.tank_speedX = 0 #скорость перемещения X. 0 - стоять на месте
        self.tank_speedY = 0 #скорость перемещения Y. 0 - стоять на месте
        self.move_speed = 3 #базовая скорость
        self.tank_startX = topleft [0] # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.tank_startY = topleft [1] #___----____----____

    ##**********************************************************

    def collide(self,tank_speedX,tank_speedY,platforms):
        for p in platforms :
            if sprite.collide_rect(self, p):
                if tank_speedX > 0:
                    self.rect.right = p.rect.left

                if tank_speedX < 0:
                    self.rect.left = p.rect.right

                if tank_speedY > 0:
                    self.rect.bottom = p.rect.top

                if tank_speedY < 0:
                    self.rect.top = p.rect.bottom

# direction constants
(DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) = range(4)

class Player(Tank):
    def __init__(self,topleft):
        Tank.__init__(self,topleft)
        self.filename = 'block/world01/block_10.bmp'
        self.image = image.load(self.filename)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.bullet = pygame.sprite.Group()
        self.direction = DIR_UP# положение танка (вверх,вниз и.т.д)
        self.timer = pygame.time.Clock()

    def shot_bull(self):
        self.bullet.add(Bullet((self.rect.center),self.direction))

    def ret_bull(self):
        return self.bullet

    def bull_move(self):
        for a in self.bullet:
            a.move()

    def tank_update(self,left,right,up,down,space,platforms):

        if left:
            self.tank_speedX = -self.move_speed # Лево = x- n
            self.tank_speedY = 0
            self.direction = DIR_LEFT

        if right:
            self.tank_speedX = self.move_speed # Право = x + n
            self.tank_speedY = 0
            self.direction = DIR_RIGHT

        if up:
            self.tank_speedY = -self.move_speed # Вверх = у- п
            self.tank_speedX = 0
            self.direction = DIR_UP

        if down:
            self.tank_speedY = self.move_speed # Вниз = у+ п
            self.tank_speedX = 0
            self.direction = DIR_DOWN

        #if space:
            #self.shot_bull()
            #print 'Shott *********'

        if not(left or right): # стоим, когда нет указаний идти
            self.tank_speedX = 0

        if not(up or down): # стоим, когда нет указаний идти
            self.tank_speedY = 0

        self.rect.left += self.tank_speedX # переносим свои положение на tank_speedX
        self.collide(self.tank_speedX,0,platforms)
        self.rect.top += self.tank_speedY # переносим свои положение на tank_speedY
        self.collide(0,self.tank_speedY,platforms)
