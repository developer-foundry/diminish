import urwid

from tui.components.headerComponent import HeaderComponent

class DashboardView(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        header = HeaderComponent(f'Dashboard - {self.model.mode.title()}', 'banner')

        menu = urwid.Text([
            u'Press (', ('refresh button', u'S'), u') to manually refresh. ',
            u'Press (', ('quit button', u'Q'), u') to quit.'
        ])
        
        quote_text = urwid.Text(u'Press (R) to get your first quote!')
        quote_filler = urwid.Filler(quote_text, valign='top', top=1, bottom=1)
        v_padding = urwid.Padding(quote_filler, left=1, right=1)
        quote_box = urwid.LineBox(v_padding)

        layout = urwid.Frame(header=header, body=quote_box, footer=menu)
        return layout
