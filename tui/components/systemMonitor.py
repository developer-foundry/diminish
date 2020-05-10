import urwid
from pyspectator.processor import Cpu
from pyspectator.memory import VirtualMemory

class SystemMonitor(urwid.LineBox):
    def __init__(self, monitorType, style, title):
        self.monitorType = monitorType
        self.cpu = Cpu(monitoring_latency=1)
        self.memory = VirtualMemory(monitoring_latency=1)
        self.monitor_text = urwid.Text(self.getText(self.monitorType), align="center")
        attMap = urwid.AttrMap(self.monitor_text, style)
        urwid.LineBox.__init__(self, attMap, title=title)
    
    def getText(self, monitorType):
        if monitorType == "cpu":
            return str(self.cpu.load)
        if monitorType == "memory":
            return str(self.memory.used_percent)
        else:
            return 'N/A'

    def refresh(self):
        self.monitor_text.set_text(self.getText(self.monitorType))
