#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import cPickle
import uuid

class ServerFactory(Factory):
    def __init__(self, gs):
        self.count_users = 0
        self.users ={} # Сохраняются все пользоватили которые на сервере
        self.games = []
        self.gs = gs

    def buildProtocol(self, addr):
        #сделать сохранение адресов клиентов
        return ServerProtocol(self,self.gs)

class ServerProtocol(Protocol):
    def __init__(self, factory,gs):
        self.factory = factory
        self.data = {}
        self.gs = gs

    def connectionMade(self):
        print "********* Connection made *********"
        id = uuid.uuid4()
        self.data['id'] = id
        self.data['type'] = 'start'
        self.sendData(self.data)

        #  Запускает цыкл игры из нескольких игроков(в многорежимной игре)
        lc = LoopingCall(self.gs.tick)
        lc.start(1/60)
        print '***Start Loop for', id

    def connectionLost(self, reason):
        print "*******Connetion lost %s" % reason

    def dataReceived(self,data):
        #print "Data recieved"
        s = cPickle.loads(data)
        self.factory.gs.parseData(s)
        #print s

    def sendData(self,data):
        print "Send data"
        s = cPickle.dumps(data,2)
        self.transport.write(s)



if __name__ == '__main__':
    reactor.listenTCP(3113,ServerFactory())
    reactor.run()
