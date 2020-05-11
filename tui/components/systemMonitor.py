import urwid
from pyspectator.processor import Cpu
from pyspectator.memory import VirtualMemory
from pyspectator.network import NetworkInterface
from random import randint

class SystemMonitor(urwid.LineBox):
    def __init__(self, monitorType, style, title):
        self.monitorType = monitorType
        self.monitor_text = urwid.Text('', align="center")
        attMap = urwid.AttrMap(self.monitor_text, style)
        urwid.LineBox.__init__(self, attMap, title=title)
    
    def getText(self, monitorType):
        cpu = Cpu(monitoring_latency=1)
        memory = VirtualMemory(monitoring_latency=1)
        network = NetworkInterface(monitoring_latency=1)
        if monitorType == "cpu":
            return str(cpu.load)
        if monitorType == "memory":
            return str(memory.used_percent)
        if monitorType == "networkreceived":
            return f'{network.bytes_recv // 1000 :,}'
        if monitorType == "networksent":
            return f'{network.bytes_sent // 1000 :,}'
        else:
            return 'N/A'

    def refresh(self):
        self.monitor_text.set_text(self.getText(self.monitorType))
