import urwid
from tui.views.signalGraph import SignalGraph
from tui.views.loggingView import LoggingView
from tui.views.systemMonitors import SystemMonitors


class LiveDashboardData(urwid.WidgetWrap):
    """
    LiveDashboardData contains the monitoring widgets for the
    ANC algorithm and the logging widget to determine status or
    errors while the algorithm is running. This view is display
    when the mode is 'live'.
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
        self.errorSignal = SignalGraph(
            self.model, 'errorBuffer', 'Error Microphone', 5, 1)
        self.referenceSignal = SignalGraph(
            self.model, 'referenceBuffer', 'Reference Microphone', 5, 1)
        self.outputSignal = SignalGraph(
            self.model, 'outputBuffer', 'Output Speaker', 5, 1)
        self.logging = LoggingView(self.model, 20)
        self.systemMonitors = SystemMonitors(self.model)

        l = [
            self.errorSignal,
            self.referenceSignal,
            self.outputSignal,
            self.logging,
            self.systemMonitors
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
        self.errorSignal.refresh()
        self.referenceSignal.refresh()
        self.outputSignal.refresh()
        self.logging.refresh()
        self.systemMonitors.refresh()
