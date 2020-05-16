import urwid
from tui.views.dashboardControls import DashboardControls
from tui.views.liveDashboardData import LiveDashboardData
from tui.views.prerecordedDashboard import PrerecordedDashboardData

class DashboardBody(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        self.displayedDashboard = 'empty'
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        self.controls = DashboardControls(self.model)
        self.liveDashboard = LiveDashboardData(self.model)
        self.prerecordedDashboard = PrerecordedDashboardData(self.model)
        self.emptyDashboard = urwid.Pile([])

        self.data = urwid.WidgetPlaceholder(self.emptyDashboard)
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

        #check and see if the model has changed and 
        if(self.model.running):
            if(self.model.mode == 'live'):
                self.data._set_original_widget(self.liveDashboard)
                self.liveDashboard.refresh()
            elif(self.model.mode == 'prerecorded'):
                self.data._set_original_widget(self.prerecordedDashboard)
                self.prerecordedDashboard.refresh()
        else:
            self.data._set_original_widget(self.emptyDashboard)
