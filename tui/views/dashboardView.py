import urwid

from tui.components.headerComponent import HeaderComponent
from tui.components.footerComponent import FooterComponent
from tui.views.dashboardBody import DashboardBody

class DashboardView(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        header = HeaderComponent(f'Dashboard - {self.model.mode.title()}', 'header')
        footer = FooterComponent([
            u'Press (', ('runButton', u'R'), u') to run algorithm.',
            u' Press (', ('quitButton', u'Q'), u') to quit.'
        ], 'footer')
        body = DashboardBody(self.model)

        layout = urwid.Frame(header=header, body=body, footer=footer)
        return layout
