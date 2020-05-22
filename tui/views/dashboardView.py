import urwid

from tui.components.headerComponent import HeaderComponent
from tui.components.footerComponent import FooterComponent
from tui.views.dashboardBody import DashboardBody


class DashboardView(urwid.WidgetWrap):
    """
    DashboardView is the primary view of the application. It contains
    a Header, Body, and Footer. The model must be passed to all
    child views and each child view must have a refresh function.
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
        header = HeaderComponent(
            f'Dashboard - {self.model.mode.title()}', 'header')
        footer = FooterComponent([
            u'Press (', ('runButton', u'R'), u') to run algorithm.',
            u' Press (', ('runButton', u'P'), u') to pause/resume algorithm.',
            u' Press (', ('quitButton', u'Q'), u') to quit.'
        ], 'footer')

        self.body = DashboardBody(self.model)

        layout = urwid.Frame(header=header, body=self.body, footer=footer)
        return layout

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
        self.body.refresh()
