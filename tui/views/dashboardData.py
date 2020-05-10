import urwid
from tui.components.headerComponent import HeaderComponent
from tui.views.signalGraph import SignalGraph
from tui.views.loggingView import LoggingView
from tui.views.systemMonitors import SystemMonitors

class DashboardData(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        header = HeaderComponent(f'Data View', 'header')
        self.errorSignal = SignalGraph(self.model, 'Error Microphone')
        self.logging = LoggingView(self.model)
        self.systemMonitors = SystemMonitors(self.model)

        l = [
            header,
            self.errorSignal,
            self.logging,
            self.systemMonitors
            ]

        w = urwid.Filler(urwid.Pile(l), 'top')
        return w

    def refresh(self):
        self.errorSignal.refresh()
        self.logging.refresh()
        self.systemMonitors.refresh()
        