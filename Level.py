#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, pygame
from pygame import *
from Block import *

class Level():
    def __init__(self, filename):
        self.filename = filename
        #self.tile_image = pygame.image.load('block/world01/block_01.bmp')
        #self.tile_image2 = pygame.image.load('platform.png')
        self.title_size = 32
        self.data= []
        self.tiles = [] # Массив всех тайлов уровня(тайл - в данном случае, кирпич из которого строятся стенки уровня)"""
        #self.tiles2 = []
        #self.platforms = [] # то, во что мы будем врезаться или опираться

    def load_level(self): # Загружает уровень из файла уровня
        #filename = "level1.txt"
        if (not os.path.isfile(self.filename)): # Выходим из программы, если файла нет
            quit()
        f = open(self.filename, "r")
        self.data = f.read().split("\n") # data - массив строчек файла

        x,y =0,0
        for row in self.data:
            for col in row:
                if col=="*":
                    sp = Block(x,y,'block/world01/block_01.bmp')
                    self.tiles.append(sp)
                if col=="#":
                    pf = Block(x,y,'platform.png')
                    self.tiles.append(pf)
                x += self.title_size
            y += self.title_size
            x=0

        f.close()

    def ret_tiles(self):
        return self.tiles
