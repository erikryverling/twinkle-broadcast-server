import getopt
import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

DEFAULT_URL = "ws://localhost:9000"

class BroadcastServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, msg, binary):
        self.factory.broadcast(msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []

    def register(self, client):
       if not client in self.clients:
            print("Registered client " + client.peerstr)
            self.clients.append(client)

    def unregister(self, client):
       if client in self.clients:
            print ("Unregistered client " + client.peerstr)
            self.clients.remove(client)

    def broadcast(self, msg):
        print ("Broadcasting message '%s' .." % msg)
        for client in self.clients:
            client.sendMessage(msg)
            print ("Message sent to " + client.peerstr)

if __name__ == '__main__':
    url = DEFAULT_URL

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"h",["url=", "help"])
    except getopt.GetoptError:
        print('twinkle-broadcast-server [--url=<url to web socket server>] [-h|--help]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('twinkle-broadcast-server [--url=<url to web socket server>] [-h|--help]')
            sys.exit()
        elif opt in ("--url"):
            url = arg

    # TODO Benifits of prepared server?
    # ServerFactory = BroadcastPreparedServerFactory

    factory = BroadcastServerFactory(url)
    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions(allowHixie76 = True)
    listenWS(factory)
    reactor.run()
