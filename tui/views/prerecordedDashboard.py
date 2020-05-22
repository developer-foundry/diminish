import urwid
from tui.views.signalGraph import SignalGraph
from tui.views.loggingView import LoggingView
from tui.views.systemMonitors import SystemMonitors


class PrerecordedDashboardData(urwid.WidgetWrap):
    """
    PrerecordedDashboardData contains the logging widget to determine status or
    errors while the algorithm is running. This view is display
    when the mode is 'prerecorded'.
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
        self.logging = LoggingView(self.model, 20)

        l = [
            self.logging
        ]

        w = urwid.Filler(urwid.Pile(l), 'top')
        return w

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
        self.logging.refresh()
