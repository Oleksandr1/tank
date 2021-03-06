#!/usr/bin/env python
# -*- coding: utf-8 -*-



#from main import GameSpace
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import cPickle

import sys

## Connection factory for the client
class ClientConnFactory(ClientFactory):
	# Just save the gs on init
	def __init__(self, gs):
		self.gs = gs

	# Save the connection, passing it the gs
	def buildProtocol(self, addr):
		print "Bild protocol"
		self.addr = addr
		self.conn = ClientConnection(addr, self.gs)
		return self.conn

# Connection for the client
class ClientConnection(Protocol):
	# Save the addr, gs on init
	def __init__(self, addr, gs):
		self.addr = addr
		self.gs = gs

	# On connection, start the game, add the looping call
	# This ensures the game will run indefinitely (at least on twisted's end)
	def connectionMade(self):
		print "connection made"
		#self.dataReceived(self)
		self.gs.play_game()
		#self.gs.sendData("Connected")
		lc = LoopingCall(self.gs.tick)
		lc.start(1/60)
		print 'AFTER START LOOOP'

	# When you get data, send it to the gamespace
	def dataReceived(self, data):
		tmp = cPickle.loads(data)
		print "GET", tmp
		self.gs.getData(tmp)
		#self.gs.getData(data)

	# Send data through the connection
	def send(self, data):
#		d = {'data':data, 'type':'game'}
#		print 'try to send:', d
		s = cPickle.dumps(data,2)
		print sys.getsizeof(data), '    ', sys.getsizeof(s)
		self.transport.write(s)
	# connection lost

	def connectionLost(self, reason):
		print "lost connection"
