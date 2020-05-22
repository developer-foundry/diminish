import urwid


class ErrorPercentage(urwid.WidgetWrap):
    """
    ErrorPercentage contains a Box widget that renders
    the current error rate for the ANC algorithm
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
        bt = urwid.BoxAdapter(urwid.LineBox(bt, "Error Rate"), 7)

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
        percentage = "{0:1.3f}".format(self.model.errorPercentage)
        self.bigtext.set_text(percentage)

        if(self.model.errorPercentage >= 0.001):
            self.attribute.set_attr('bigtextbad')
        else:
            self.attribute.set_attr('bigtextgood')
