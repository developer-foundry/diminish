import urwid
from tui.components.headerComponent import HeaderComponent
from tui.components.footerComponent import FooterComponent
from tui.components.positiveNegativeBarGraph import PositiveNegativeBarGraph


class SignalGraph(urwid.WidgetWrap):
    """
    SignalGraph is a container view that uses a HeaderComponent
    and a LineBox to display a live graph of incoming data
    from the ANC algorithm. Generally, the graph is updated every
    one second, but can be tweaked through configuring the 
    {guiRefreshTimer}
    """

    def __init__(self, model, signal, name, height, barWidth):
        """
        Parameters
        ----------
        model : ConfigurationModel
            The model that this component is linked to.
        signal : np.array
            The attribute in the model used to store data that will be graphed
        name : str
            The name of the graph to display at the top of the graph
        height : int
            The number of rows to use to display the graph.
        barWidth : int
            The widget of each bar to be rendered
        """
        self.model = model
        self.name = name
        self.signal = signal
        self.height = height
        self.barWidth = barWidth
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        """
        Composes child views and components into a single object to be rendered.
        Uses a custom widget PositiveNegativeBarGraph that is a fork of the
        urwid BarGraph widget

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
        header = HeaderComponent(f'{self.name.title()} Signal', 'h2')
        self.bg = PositiveNegativeBarGraph(['bg background', 'bg 1'])
        self.bg.set_bar_width(self.barWidth)
        body = urwid.BoxAdapter(self.bg, self.height)

        l = [header, body]
        w = urwid.Pile(l)
        b = urwid.LineBox(w)
        return b

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
        data = getattr(self.model, self.signal)
        size = self.bg.maxcol if self.bg.maxcol is not None else len(data)
        start = len(data) - size
        self.bg.set_data(data[start:], self.model.graphTop,
                         self.model.graphBottom)
