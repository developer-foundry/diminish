import urwid


class SystemMonitor(urwid.LineBox):
    """
    The SystemMonitor component represents a box displaying a value being monitored in the system like cpu or memory usage
    """

    def __init__(self, model, monitorType, style, title):
        """
        Parameters
        ----------
        model : ConfigurationModel
            The model that this component is linked to.
        monitorType : str
            The attribute in the model that this component is linked to. i.e. self.mode['cpu']
        style : str
            The style used by urwid to apply to the label text
        title : str
            The title of the box that wraps the system monitor value.
        """
        self.model = model
        self.monitorType = monitorType
        self.monitor_text = urwid.Text('', align="center")
        attMap = urwid.AttrMap(self.monitor_text, style)
        urwid.LineBox.__init__(self, attMap, title=title)

    def refresh(self):
        """
        Updates the component underlying widget display values based on the model changing

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
        self.monitor_text.set_text(str(getattr(self.model, self.monitorType)))
