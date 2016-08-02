#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, math, pygame
from pygame import *

# direction constants
(DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) = range(4)

class Bullet(sprite.Sprite):



    def __init__(self,center,direction,filename = 'gun.png'):
        sprite.Sprite.__init__(self)
        self.filename = filename
        self.image = image.load('bullet03.tga').convert()
        self.image2 = image.load('bullet03.tga').convert()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed =3
        self.direction = direction


    def move (self):

        if self.direction == DIR_UP:
            self.image = transform.rotate(self.image2,90)
            self.rect.topleft = [self.rect.left, self.rect.top - self.speed]

            #self.image = transform.rotate(self.image2,90)
            #self.rect = self.image.get_rect()
            #self.rect.top -= self.speed

        if self.direction == DIR_RIGHT:
            #self.image = image.load('bullet03.tga')
            self.rect.topleft = [self.rect.left + self.speed, self.rect.top]

        if self.direction == DIR_LEFT:
            self.image = transform.rotate(self.image2,180)
            self.rect.topleft = [self.rect.left - self.speed, self.rect.top]

        if self.direction == DIR_DOWN:
            self.image = transform.rotate(self.image2,270)
            self.rect.topleft = [self.rect.left, self.rect.top + self.speed]
