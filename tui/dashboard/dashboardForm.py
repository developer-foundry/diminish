import urwid

class DashboardForm():
    # Tuples of (Key, font color, background color)
    palette = [
        ('titlebar', 'dark red', ''),
        ('refresh button', 'dark green,bold', ''),
        ('quit button', 'dark red', ''),
        ('getting quote', 'dark blue', ''),
        ('headers', 'white,bold', ''),
        ('change ', 'dark green', ''),
        ('change negative', 'dark red', '')]

    # Notice "refresh button" and "quit button" keys were defined above in the color scheme.
    menu = urwid.Text([
        u'Press (', ('refresh button', u'R'), u') to manually refresh. ',
        u'Press (', ('quit button', u'Q'), u') to quit.'
    ])

    def __init__(self):
        self.log = urwid.SimpleFocusListWalker([])
        header_text = urwid.Text(u' Stock Quotes')
        header = urwid.AttrMap(header_text, 'titlebar')

        quote_text = urwid.Text(u'Press (R) to get your first quote!')
        quote_filler = urwid.Filler(quote_text, valign='top', top=1, bottom=1)
        v_padding = urwid.Padding(quote_filler, left=1, right=1)
        quote_box = urwid.LineBox(v_padding)

        # Assemble the widgets
        self.layout = urwid.Frame(header=header, body=quote_box, footer=self.menu)