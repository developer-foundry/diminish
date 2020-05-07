import urwid
from tui.components.headerComponent import HeaderComponent

class DashboardData(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        header = HeaderComponent(f'Data View', 'header')

        l = [
            header,
            header
            ]

        w = urwid.Filler(urwid.Pile(l))
        return w
