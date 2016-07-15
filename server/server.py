from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

PORT = 2512
class ClientProtocol(LineReceiver):
    def __init__(self,factory):
        self.factory = factory
        self.id = None
        self.name = None
        self.state = "REGISTER"

    def connectionMade(self):
        self.sendLine("What`s your name?")

    def connectionLost(self, reason):
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.broadcastMessage('%s has left the channel.' % (self.name,))

    def lineReceived(self, line):
        if self.state == 'REGISTER':
            self.handle_REGISTER(line)
        else:
            self.handle_CONNECTION(line)

    def handle_REGISTER(self, name):
        if name in self.factory.users:
            self.sendLine("Name taken, choose another")
            return
        self.sendLine("Welcome %s" % (name,))
        self.broadcastMessage('%s has connected to the channel' %(name,))
        self.name = name
        self.factory.users[name]=self
        self.state = "ONLINE"

    def handle_CONNECTION(self, message):
        print message

        if message == "quit" and self.name == 'sanya':
            reactor.stop()

        message = "%s  %s" %(self.name, message)
        self.broadcastMessage(message)

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)

class GameFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ClientProtocol(self)


if __name__ == '__main__':
    print 'Server started on %s' % (PORT,)

    reactor.listenTCP(PORT,GameFactory())
    reactor.run()

    print 'Server stopped by admin'
