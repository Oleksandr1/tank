#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *

MOVE_SPEED = 5
WIDTH = 30
HEIGHT = 30
COLOR = '#FFFF00'
BARREL_WIDTH = 10
BARREL_HEIGHT = 10
BARREL_COLOR = '#FF2B2B'
class Tank(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.startX = x
        self.startY = y
        self.side = 'up'
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x,y,WIDTH,HEIGHT)

        self.barrel = Surface((BARREL_WIDTH, BARREL_HEIGHT))
        self.barrel.fill(Color(BARREL_COLOR))
        #self.barrel_rect = Rect((x/2- BARREL_WIDTH/2),(y/2 - BARREL_HEIGHT/2),BARREL_WIDTH,BARREL_HEIGHT)

    def update(self, left, right, up, down, platforms):
        if left:
            self.xvel = -MOVE_SPEED
            self.yvel = 0
            self.side = 'left'

        if right:
            self.xvel = MOVE_SPEED
            self.yvel = 0
            self.side = 'right'

        if up:
            self.yvel = -MOVE_SPEED
            self.xvel = 0
            self.side = 'up'

        if down:
            self.yvel = MOVE_SPEED
            self.xvel = 0
            self.side = 'down'


        if not(left or right):
            self.xvel = 0

        if not(up or down):
            self.yvel = 0

        self.rect.x +=self.xvel
        self.collide(self.xvel,0,platforms)
        self.rect.y +=self.yvel
        self.collide(0,self.yvel,platforms)

    def collide(self, xvel, yvel,platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top

                if yvel < 0:
                    self.rect.top = p.rect.bottom
