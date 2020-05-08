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
        data = [ [0.005], [-0.005], [0.005], [-0.005], [0.005], [-0.005], [0.005], [-0.005], [0.005], [-0.005], [0.005], [-0.005], [0.005], [-0.005]]
        bg = PositiveNegativeBarGraph(['bg background','bg 1'])
        bg.set_data(data, 0.01, -0.01)
        bg.set_bar_width(1)
        body = urwid.BoxAdapter(bg, 10) #maxrow has to be divisible by 2

        l = [header,body]
        w = urwid.Pile(l)
        b = urwid.LineBox(w)
        return b
