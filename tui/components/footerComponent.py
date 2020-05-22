import urwid


class FooterComponent(urwid.AttrMap):
    """
    The FooterComponent wraps a Text widget to used at the bottom of a urwid.Frame
    """

    def __init__(self, markup, style):
        """
        Parameters
        ----------
        markup : str
            The urwid markup used to create the Text widget.
        style : str
            The style to apply to the Text widget
        """
        header_text = urwid.Text(markup)
        urwid.AttrMap.__init__(self, header_text, style)
