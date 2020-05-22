import urwid


class StatusView(urwid.WidgetWrap):
    """
    StatusView is a view to display to the user whether 
    or not the algorithm is paused or not.
    """

    def __init__(self, model):
        """
        Parameters
        ----------
        model : ConfigurationModel
            The model that this component is linked to.
        """
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        """
        Composes child views and components into a single object to be rendered.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.bigtext = urwid.BigText("", urwid.HalfBlock5x4Font())
        bt = urwid.Padding(self.bigtext, 'center', None)
        self.attribute = urwid.AttrWrap(bt, 'bigtextgood')
        bt = urwid.Filler(self.attribute, 'bottom', None, 7)
        bt = urwid.BoxAdapter(urwid.LineBox(bt, "Status"), 7)

        return bt

    def refresh(self):
        """
        Updates the view and any child views based on the model changing

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        state = "On"if not self.model.paused else "Off"
        self.bigtext.set_text(state)

        if(self.model.paused):
            self.attribute.set_attr('bigtextbad')
        else:
            self.attribute.set_attr('bigtextgood')
