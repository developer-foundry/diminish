import urwid


class LoggingView(urwid.WidgetWrap):
    """
    LoggingView contains a Box widget that renders all logging messages
    for the TUI and CLI processes to the screen.
    """

    def __init__(self, model, height):
        """
        Parameters
        ----------
        model : ConfigurationModel
            The model that this component is linked to.
        """
        self.model = model
        self.height = height
        self.entries = urwid.SimpleFocusListWalker(
            self.convert(self.model.logEntries))
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
        return urwid.BoxAdapter(urwid.LineBox(urwid.ListBox(self.entries), title="Logging"), self.height)

    def convert(self, entries):
        """
        Converts an array of text strings to urwid Text widgets

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
        textArray = []
        for entry in entries:
            textArray.append(urwid.Text(entry))
        return textArray

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
        self.entries.clear()
        self.entries.extend(self.convert(self.model.logEntries))
