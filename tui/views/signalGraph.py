import urwid
from tui.components.headerComponent import HeaderComponent
from tui.components.footerComponent import FooterComponent

class SignalGraph(urwid.WidgetWrap):
    def __init__(self, model, name):
        self.model = model
        self.name = name
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        header = HeaderComponent(f'{self.name.title()} Signal', 'h2')
        data = [ [10,0], [20,0], [50,0], [20,0], [60,0], [80,0], [10,0]]
        bg = urwid.BarGraph(['bg background','bg 1','bg 1'])
        bg.set_data(data, 100, [10,20,30,40,50,60,70,80,90])
        body = urwid.BoxAdapter(bg, 10)

        l = [header,body]
        w = urwid.Pile(l)
        b = urwid.LineBox(w)
        return b
