import urwid

class DashboardControls(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        quote_text = urwid.Text(u'Controls!')
        quote_filler = urwid.Filler(quote_text, valign='top', top=1, bottom=1)
        return quote_filler
