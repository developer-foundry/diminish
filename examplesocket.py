import bluetooth
from twisted.internet import abstract, fdesc

class ExampleSocket(abstract.FileDescriptor):
  def __init__(self, protocol, reactor):
    self.uuid = '87f39d29-7d6d-437d-973b-fba39e49d4ee'
    self.connected = False
    self.protocol = protocol
    self.reactor = reactor
    
    abstract.FileDescriptor.__init__(self, reactor)
    
    self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    self.sock.bind(('', bluetooth.PORT_ANY))
    self.sock.listen(1)

    port = self.sock.getsockname()[1]

    bluetooth.advertise_service(self.sock, 'ANCServer', service_id=self.uuid,
                                service_classes=[self.uuid, bluetooth.ADVANCED_AUDIO_CLASS],
                                profiles=[bluetooth.ADVANCED_AUDIO_PROFILE]
                                )

    client_sock, client_info = self.sock.accept()
    print("client connected")
    self.sock.setblocking(1)
    self.connected = True
    self.protocol.makeConnection(self)
    self.startReading()
  
  def fileno(self):
    return self.sock.fileno()
    
  def writeSomeData(self, data):
    print('writing')
    return fdesc.writeToFD(self.fileno(), data)
  
  def doRead(self):
    print('reading')
    return fdesc.readFromFD(self.fileno(), self.protocol.dataReceived)
  
  def connectionLost(self, reason):
    abstract.FileDescriptor.connectionLost(self, reason)
    self.sock.close()
    self.connected = False
    self.protocol.connectionLost(reason)