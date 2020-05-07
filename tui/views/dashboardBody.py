import urwid
from tui.views.dashboardControls import DashboardControls
from tui.views.dashboardData import DashboardData

class DashboardBody(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        controls = DashboardControls(self.model)
        data = DashboardData(self.model)
        vline = urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')
        body = urwid.Columns([
                (30, controls), #30 is number of columns wide
                ('fixed',1,vline), #fixed means it can't move
                ('weight',2,data) #weight means 'fill in the rest of the screen'
            ],
            dividechars=1, focus_column=2)
        return body
