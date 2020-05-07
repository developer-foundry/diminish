import urwid

class HeaderComponent(urwid.AttrMap):
    def __init__(self, markup, style):
        header_text = urwid.Text(markup, align="center")
        urwid.AttrMap.__init__(self, header_text, style)
