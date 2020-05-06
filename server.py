from examplesocket import ExampleSocket
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver

class exampleProtocol(LineReceiver):
  def setChannel(self, channel, value):
    print(f'Channel: {channel}')
    print(f'Value: {value}')
    #self.sendLine(f'SEND {channel}:{value}')
    print(f'>> SEND {channel}')

  def lineReceived(self, line):
    print(f'<< {line}')

  def connectionMade(self):
    print('Connection made')

  def connectionLost(self,reason):
    print(f'Connection lost: {reason}')

if __name__ == "__main__":
  proto=exampleProtocol()
  bt=ExampleSocket(proto, reactor)

  reactor.run()