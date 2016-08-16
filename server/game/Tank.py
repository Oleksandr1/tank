#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, random, pygame
from pygame import *
from Block import *
from Bullet import *

# direction constants
(DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT) = range(4)

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

class Player(Tank):
    def __init__(self,topleft):
        Tank.__init__(self,topleft)
        self.direction = DIR_UP# положение танка (вверх,вниз и.т.д
        self.image = image.load('Tpic/GTankU1.png')
        self.image2 = image.load('Tpic/GTankU1.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.bullet = pygame.sprite.Group()


    def shot_bull(self):
        self.bullet.add(Bullet((self.rect.center),self.direction))

    def ret_bull(self):
        return self.bullet

    def ret_position(self):
        return self.rect.center

    def bull_move(self):
        for a in self.bullet:
            a.move()

    def del_bull (self):
        for a in self.bullet:
            if a.rect.left > (800 - a.rect.width):
                a.kill()
                return
            if a.rect.top < 0:
                a.kill()
                return
            if a.rect.left < 0:
                a.kill()
                return
            if a.rect.top > (700 - a.rect.height):
                a.kill()
                return

    def tank_update(self,left,right,up,down,space,platforms):

        if left:
            self.tank_speedX = -self.move_speed # Лево = x- n
            self.tank_speedY = 0
            self.direction = DIR_LEFT
            self.image = transform.rotate(self.image2,90)

        if right:
            self.tank_speedX = self.move_speed # Право = x + n
            self.tank_speedY = 0
            self.direction = DIR_RIGHT
            self.image = transform.rotate(self.image2,270)

        if up:
            self.tank_speedY = -self.move_speed # Вверх = у- п
            self.tank_speedX = 0
            self.direction = DIR_UP
            self.image = transform.rotate(self.image2,0)

        if down:
            self.tank_speedY = self.move_speed # Вниз = у+ п
            self.tank_speedX = 0
            self.direction = DIR_DOWN
            self.image = transform.rotate(self.image2,180)

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

    ##EnemyEnemyEnemyEnemyEnemyEnemyEnemyEnemyEnemyEnemyEnemy
class Enemy(Tank):
    def __init__(self,topleft):
        Tank.__init__(self,topleft)
        self.direction = DIR_UP# положение Enemy (вверх,вниз и.т.д
        self.image = image.load('Tpic/En2ShellT1.png')
        self.image2 = image.load('Tpic/En2ShellT1.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.move_speed = 1 #базовая скорость
        self.enemy_life = True
        self.s=0


    def DIR_UP(self):

        self.tank_speedY = -self.move_speed # Вверх = у- п
        self.tank_speedX = 0
        self.image = transform.rotate(self.image2,0)

    def DIR_DOWN(self):
        self.tank_speedY = self.move_speed # Вниз = у+ п
        self.tank_speedX = 0
        self.image = transform.rotate(self.image2,180)

    def DIR_LEFT(self):

        self.tank_speedX = -self.move_speed # Лево = x- n
        self.tank_speedY = 0
        self.image = transform.rotate(self.image2,90)

    def DIR_RIGHT(self):
        self.tank_speedX = self.move_speed # Право = x + n
        self.tank_speedY = 0
        self.image = transform.rotate(self.image2,270)

    def collide_OBJ(self,platforms):
        x=self.rect.left
        y=self.rect.top

        new_pos_rect = Rect((x-1,y-1),(42,42))

        for p in platforms :
            if Rect.colliderect(new_pos_rect,p.rect):
                return True

    def collide_UP(self,tank_speedX,tank_speedY,platforms):
        x=self.rect.left
        y=self.rect.top

        new_pos_rect = Rect((x,y-1),(42,42))

        for p in platforms :
            if Rect.colliderect(new_pos_rect,p.rect):
                if tank_speedY < 0:
                    return True

    def collide_DOWN(self,tank_speedX,tank_speedY,platforms):
        x=self.rect.left
        y=self.rect.top

        new_pos_rect = Rect((x,y+2),(40,40))

        for p in platforms :
            if Rect.colliderect(new_pos_rect,p.rect):
                if tank_speedY > 0:
                    return True

    def collide_LEFT(self,tank_speedX,tank_speedY,platforms):
        x=self.rect.left
        y=self.rect.top

        new_pos_rect = Rect((x-1,y),(40,40))

        for p in platforms :
            if Rect.colliderect(new_pos_rect,p.rect):
                if tank_speedX < 0:
                    return True

    def collide_RIGHT(self,tank_speedX,tank_speedY,platforms):
        x=self.rect.left
        y=self.rect.top

        new_pos_rect = Rect((x+1,y),(40,40))

        for p in platforms :
            if Rect.colliderect(new_pos_rect,p.rect):
                if tank_speedX > 0:
                    return True


    def enemy_target(self,platforms):
        #(DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT) = range(4)
        #print self.collide_UP(0,self.tank_speedY,platforms)
        #print self.collide_LEFT(self.tank_speedX,0,platforms)
        if self.direction == DIR_UP:
            if not self.collide_UP(0,self.tank_speedY,platforms):
                self.DIR_UP()
            else:
                self.direction = DIR_LEFT#random.randint(DIR_RIGHT,DIR_LEFT)

        if self.direction == DIR_LEFT:
            if self.collide_OBJ(platforms):
                if not self.collide_LEFT(self.tank_speedX,0,platforms):
                    self.DIR_LEFT()
                else:
                    self.direction = DIR_RIGHT#random.randint(DIR_DOWN,DIR_RIGHT)
            else:
                self.direction = DIR_UP

        if self.direction == DIR_RIGHT:
            if self.collide_OBJ(platforms):
                if not self.collide_RIGHT(self.tank_speedX,0,platforms):
                    self.DIR_RIGHT()
                else:
                    self.direction = DIR_DOWN
            else:
                self.direction = DIR_UP

        if self.direction == DIR_DOWN:
            if not self.collide_DOWN(0,self.tank_speedY,platforms):
                self.DIR_DOWN()
            else:
                self.direction = DIR_LEFT#random.randint(DIR_RIGHT,DIR_LEFT)

        if self.direction ==-1:#Тест
            self.tank_speedX=0
            self.tank_speedY=0


        self.rect.left += self.tank_speedX # переносим свои положение на tank_speedX
        self.rect.top += self.tank_speedY # переносим свои положение на tank_speedY
