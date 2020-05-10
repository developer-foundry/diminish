import urwid
from tui.components.headerComponent import HeaderComponent
from tui.components.footerComponent import FooterComponent
from tui.components.positiveNegativeBarGraph import PositiveNegativeBarGraph

class SignalGraph(urwid.WidgetWrap):
    def __init__(self, model, name):
        self.model = model
        self.name = name
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        header = HeaderComponent(f'{self.name.title()} Signal', 'h2')
        self.bg = PositiveNegativeBarGraph(['bg background','bg 1'])
        self.bg.set_data(self.model.errorBuffer, self.model.graphTop, self.model.graphBottom)
        self.bg.set_bar_width(1)
        body = urwid.BoxAdapter(self.bg, 10)

        l = [header,body]
        w = urwid.Pile(l)
        b = urwid.LineBox(w)
        return b
    
    def refresh(self):
        self.bg.set_data(self.model.errorBuffer, self.model.graphTop, self.model.graphBottom)
