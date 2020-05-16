import urwid
from tui.views.signalGraph import SignalGraph
from tui.views.loggingView import LoggingView
from tui.views.systemMonitors import SystemMonitors

class PrerecordedDashboardData(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        self.logging = LoggingView(self.model, 20)

        l = [
            self.logging
            ]

        w = urwid.Filler(urwid.Pile(l), 'top')
        return w

    def refresh(self):
        self.logging.refresh()