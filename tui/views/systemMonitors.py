import urwid
from tui.components.systemMonitor import SystemMonitor

class SystemMonitors(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        self.monitors = []
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        self.cpuMonitor = SystemMonitor('cpu', 'header', 'CPU Load')
        self.memoryMonitor = SystemMonitor('memory', 'header', 'Used Memory (%)')
        self.received = SystemMonitor('networkreceived', 'header', 'Kilobytes Received')
        self.sent = SystemMonitor('networksent', 'header', 'Kilobytes Sent')

        l = [self.cpuMonitor, self.memoryMonitor, self.received, self.sent]
        return urwid.Columns(l)

    def convert(self, entries):
        textArray = []
        for entry in entries:
            textArray.append(urwid.Text(entry))
        return textArray

    
    def refresh(self):
        self.cpuMonitor.refresh()
        self.memoryMonitor.refresh()
        self.received.refresh()
        self.sent.refresh()
