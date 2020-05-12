import urwid
from tui.components.headerComponent import HeaderComponent
from tui.components.footerComponent import FooterComponent
from tui.components.positiveNegativeBarGraph import PositiveNegativeBarGraph

class SignalGraph(urwid.WidgetWrap):
    def __init__(self, model, signal, name, height, barWidth):
        self.model = model
        self.name = name
        self.signal = signal
        self.height = height
        self.barWidth = barWidth
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        header = HeaderComponent(f'{self.name.title()} Signal', 'h2')
        self.bg = PositiveNegativeBarGraph(['bg background','bg 1'])
        self.bg.set_bar_width(self.barWidth)
        body = urwid.BoxAdapter(self.bg, self.height)

        l = [header,body]
        w = urwid.Pile(l)
        b = urwid.LineBox(w)
        return b
    
    def refresh(self):
        data = getattr(self.model, self.signal)
        size = self.bg.maxcol if self.bg.maxcol is not None else len(data)
        start = len(data) - size
        self.bg.set_data(data[start:], self.model.graphTop, self.model.graphBottom)
