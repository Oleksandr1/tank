#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame import *
from twisted.internet import reactor

from connection import *
from Tank import Player, Tank
from Level import Level


HOST = 'localhost'
PORT = 3113
WIN_WIDTH = 1024
WIN_HEIGHT = 700
WIN_DISPLAY = (WIN_WIDTH,WIN_HEIGHT)
WIN_COLOR = '#AF4F5F'

class GameSpace():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tanks')
        self.screen = pygame.display.set_mode(WIN_DISPLAY)
        self.background = Surface(WIN_DISPLAY)
        self.background.fill(Color(WIN_COLOR))

        self.timer = pygame.time.Clock()

        self.cf = ClientConnFactory(self)
        reactor.connectTCP(HOST,PORT,self.cf)
        reactor.run()

    def start(self):
        self.player = Player(100,100)# инициализируем Tank
        self.level1 = Level('level1.txt')#Инициализируем level1
        self.level1.load_level()

        #self.test_loop()


    def tick(self):
        print 'tick'
        for e in pygame.event.get():
            if e.type == QUIT:
                reactor.stop()
                raise SystemExit, "Quit"
            if e.type == KEYDOWN and e.key == K_LEFT:
                print '*'*100
                print "KEYDOWN K_LEFT"
                self.sendData("KEYDOWN LEFT! Yu-hooo")
            print 'end tick for'
        #self.sendData("**********************Hello!")
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.player.image,(100,100))
        pygame.display.update()


    def sendData(self, data):
        self.cf.conn.send(data)

    def addData(self, data):
        print "INCOMING: ", data

    def test_loop(self):
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                     raise SystemExit, "QUIT"
                if e.type == KEYDOWN and e.key == K_LEFT:
                    print "KEYDOWN K_LEFT"


            self.screen.blit(self.background,(0,0))
            self.screen.blit(self.player.image,(100,100))
            pygame.display.update()


def main():
    r = GameSpace()
    r.start()

if __name__ == '__main__':
    main()
