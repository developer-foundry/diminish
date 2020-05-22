import urwid
from tui.components.systemMonitor import SystemMonitor


class SystemMonitors(urwid.WidgetWrap):
    """
    SystemMonitors is a view to track various system level
    information like CPU/Memory usage
    """

    def __init__(self, model):
        """
        Parameters
        ----------
        model : ConfigurationModel
            The model that this component is linked to.
        """
        self.model = model
        self.monitors = []
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        """
        Composes child views and components into a single object to be rendered.
        This view builds a list of System Monitors to track various system level
        information like CPU/Memory usage.

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
        self.cpuMonitor = SystemMonitor(
            self.model, 'cpu', 'header', 'CPU Load')
        self.memoryMonitor = SystemMonitor(
            self.model, 'memory', 'header', 'Used Memory (MB)')
        self.received = SystemMonitor(
            self.model, 'packetsreceived', 'header', 'Bytes Received')
        self.sent = SystemMonitor(
            self.model, 'packetssent', 'header', 'Bytes Sent')

        l = [self.cpuMonitor, self.memoryMonitor, self.received, self.sent]
        return urwid.Columns(l)

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
        self.cpuMonitor.refresh()
        self.memoryMonitor.refresh()
        self.received.refresh()
        self.sent.refresh()
