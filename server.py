#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import cPickle
import uuid
"""
    #Основные состояния(self.state) клиента
    REGISTER - резгистрация клиента
    ONLINE - в сети,он делится на:
        PLAY сама игра
            MOVE
            SHOOT
        PAUSE
        STOP
        DISCONNECT


"""

PORT = 3113
class ServerProtocol(Protocol):
    def __init__(self,factory):
        self.factory = factory

    def connectionMade(self):
        if len(self.factory.game)<10:
            print 'connectionMade'
            print 'new connection'
            ID = uuid.uuid4()
            self.sendData("You connected to server")
            self.sendData("Your ID is %s" % ID)
            self.factory.game.append(ID)
        else:
            self.sendData("Wait for connection")
        

    def connectionLost(self, reason):
        print "Connection lost with %s" % reason
        print len(self.factory.users)

    def dataReceived(self, data):
        print 'lineReceived'
        #print 'Client send %s' % data
        s = cPickle.loads(data)
        print(s)
        self.sendData(s)


    def sendData(self, data):
        s = cPickle.dumps(data)
        self.transport.write(s)


    def playGame(self):
        pass

    def pause(self):
        pass

    def stopGame(self):
        pass

class GameFactory(Factory):
    def __init__(self):
        self.users = {}
        self.game = []
       

    def buildProtocol(self, addr):
        return ServerProtocol(self)


if __name__ == '__main__':
    print 'Server started on %s' % (PORT,)
    reactor.listenTCP(PORT,GameFactory())
    reactor.run()

    print 'Server stopped by admin'
