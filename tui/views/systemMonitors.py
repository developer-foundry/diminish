import urwid
from tui.components.systemMonitor import SystemMonitor

class SystemMonitors(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        self.monitors = []
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        self.cpuMonitor = SystemMonitor(self.model, 'cpu', 'header', 'CPU Load')
        self.memoryMonitor = SystemMonitor(self.model, 'memory', 'header', 'Used Memory (MB)')
        self.received = SystemMonitor(self.model, 'packetsreceived', 'header', 'Bytes Received')
        self.sent = SystemMonitor(self.model, 'packetssent', 'header', 'Bytes Sent')

        l = [self.cpuMonitor, self.memoryMonitor, self.received, self.sent]
        return urwid.Columns(l)
    
    def refresh(self):
        self.cpuMonitor.refresh()
        self.memoryMonitor.refresh()
        self.received.refresh()
        self.sent.refresh()
