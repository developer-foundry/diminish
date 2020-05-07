import urwid

class HeaderComponent(urwid.AttrMap):
    def __init__(self, text, style):
        header_text = urwid.Text(text)
        urwid.AttrMap.__init__(self, header_text, style)
