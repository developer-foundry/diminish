import urwid
from tui.components.headerComponent import HeaderComponent
from tui.views.signalGraph import SignalGraph

class DashboardData(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        header = HeaderComponent(f'Data View', 'header')
        errorSignal = SignalGraph(self.model, 'Error Microphone')
        targetSignal = SignalGraph(self.model, 'Target File')
        referenceSignal = SignalGraph(self.model, 'Reference Microphone')
        outputSignal = SignalGraph(self.model, 'Output Spaker')
        algorithmErrorSignal = SignalGraph(self.model, 'Algorithm Error')

        l = [
            header,
            errorSignal,
            targetSignal,
            referenceSignal,
            outputSignal,
            algorithmErrorSignal,
            ]

        w = urwid.Filler(urwid.Pile(l), 'top')
        return w
