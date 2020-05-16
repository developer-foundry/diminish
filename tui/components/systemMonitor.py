import urwid

class SystemMonitor(urwid.LineBox):
    def __init__(self, model, monitorType, style, title):
        self.model = model
        self.monitorType = monitorType
        self.monitor_text = urwid.Text('', align="center")
        attMap = urwid.AttrMap(self.monitor_text, style)
        urwid.LineBox.__init__(self, attMap, title=title)
    
    def refresh(self):
        self.monitor_text.set_text(str(getattr(self.model,self.monitorType)))
