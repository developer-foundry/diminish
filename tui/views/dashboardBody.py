import urwid
from tui.views.dashboardControls import DashboardControls
from tui.views.dashboardData import DashboardData

class DashboardBody(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        self.controls = DashboardControls(self.model)
        self.data = DashboardData(self.model)
        vline = urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')
        
        body = urwid.Columns([
                (30, self.controls), #30 is number of columns wide
                ('fixed',1,vline), #fixed means it can't move
                self.data
            ],
            dividechars=1)
        return body
    
    def refresh(self):
        self.controls.refresh()
        self.data.refresh()
