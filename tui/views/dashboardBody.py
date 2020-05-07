import urwid

class DashboardBody(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        quote_text = urwid.Text(u'Press (R) to get your first quote!')
        quote_filler = urwid.Filler(quote_text, valign='top', top=1, bottom=1)
        v_padding = urwid.Padding(quote_filler, left=1, right=1)
        quote_box = urwid.LineBox(v_padding)
        return quote_box
