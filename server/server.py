#!/usr/bin/env python
# -*- coding: utf-8 -*-
from serv_conn import ServerFactory
from twisted.internet import reactor
from serv_game import OnePlayerGame
PORT = 3113

class GameServer():
    def __init__(self):
        print "Start server on %s" % PORT
        self.game = OnePlayerGame()
        self.game.play_game()
        self.serv_factory = ServerFactory(self)
        reactor.listenTCP(PORT, self.serv_factory)
        reactor.run()

        #визуализация игры на сервере


    def start(self):
        print "Game start!"

#    def getData(self, data):
#        print "get: ", data

    def tick(self):
        self.game.tick()

    def parseData(self, data):
        #print 'Parsing data: ' , data
        #print type(data)

        if data.get('type') == 'start':
            self.parseStart(data)

        if data.get('type') == 'game':
            self.parseGame(data)

        if data.get('type') == 'stop':
            self.parseStop(data)

        if data.get('type') == 'pause':
            self.parsePause(data)

        if data.get('type') == 'message':
            self.parseMessage(self, data)

        if data.get('type') == 'registration':
            self.parseRegistration(self, data)

    def parseStart(self, data):
        print 'Parse Start data'

    def parseGame(self, data):
        #print 'Parse Game'
        coord = data['coordinate']
        #print coord
        if coord[0] == 1:
            print 'turn left'
            self.game.left = True
            self.game.up=self.game.down=self.game.right=False

        if coord[1] == 1:
            print 'turn right'
            self.game.right = True
            self.game.up=self.game.down=self.game.left=False

        if coord[2] == 1:
            print 'turn top'
            self.game.up = True
            self.game.down=self.game.left=self.game.right=False

        if coord[3] == 1:
            print 'turn down'
            self.game.down = True
            self.game.up=self.game.left=self.game.right=False

        if coord == (0,0,0,0):
            print 'stopped'
            self.game.up=self.game.down=self.game.left=self.game.right=False

        if data['shoot']:
            print 'Shoot'



    def parseStop(self, data):
        print 'Parse Stop'

    def parsePause(self, data):
        print 'Parse Pause'

    def parseMessage(self, data):
        print 'Parse Message'

    def parseRegistration(self, data):
        print 'Registration'



if __name__ == '__main__':
    a = GameServer()
