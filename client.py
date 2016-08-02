from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet.task import LoopingCall

from Game import Game
import cPickle

class ClientConnFactory(ClientFactory):
	# Just save the gs on init
    def __init__(self, gs):
        self.gs = gs

        # Save the connection, passing it the gs
    def buildProtocol(self, addr):
        self.addr = addr
        self.conn = ClientConnection(addr, self.gs)
        return self.conn

class ClientConnection(Protocol):
    # Save the addr, gs on init
    def __init__(self, addr, gs):
        self.addr = addr
        self.gs = gs

	# On connection, start the game, add the looping call
	# This ensures the game will run indefinitely (at least on twisted's end)
    def connectionMade(self):
        print "connection made"
        self.gs.draw_game()
        lc = LoopingCall(self.gs.action)
        lc.start(1/60)

	# When you get data, send it to the gamespace
	def dataReceived(self, data):
        self.gs.get_data(data)

    # Send data through the connection
    def send(self, data):
        self.transport.write(data)

	# connection lost
    def connectionLost(self, reason):
        print "lost connection"
