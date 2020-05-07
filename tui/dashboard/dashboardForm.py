import urwid
from tui.palette.palette import palette

class DashboardForm():
    def __init__(self):
        header_text = urwid.Text(u' Stock Quotes')
        header = urwid.AttrMap(header_text, 'banner')

        menu = urwid.Text([
            u'Press (', ('refresh button', u'R'), u') to manually refresh. ',
            u'Press (', ('quit button', u'Q'), u') to quit.'
        ])
        
        quote_text = urwid.Text(u'Press (R) to get your first quote!')
        quote_filler = urwid.Filler(quote_text, valign='top', top=1, bottom=1)
        v_padding = urwid.Padding(quote_filler, left=1, right=1)
        quote_box = urwid.LineBox(v_padding)

        layout = urwid.Frame(header=header, body=quote_box, footer=menu)
        self.loop = urwid.MainLoop(layout, palette=palette)
    
    def run(self):
        self.loop.run()