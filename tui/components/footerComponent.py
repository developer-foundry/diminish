import urwid

class FooterComponent(urwid.AttrMap):
    def __init__(self, markup, style):
        header_text = urwid.Text(markup)
        urwid.AttrMap.__init__(self, header_text, style)
