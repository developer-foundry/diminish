import urwid
from tui.palette.palette import palette
from tui.views.dashboardView import DashboardView
from tui.models.configurationModel import ConfigurationModel

class DashboardController():
    def __init__(self, parameters):
        self.model = ConfigurationModel(parameters)
        self.view = DashboardView(self.model)
        
        self.loop = urwid.MainLoop(self.view, palette=palette, unhandled_input=self.handle_input)
    
    def run(self):
        self.loop.run()
    
    # Handle key presses
    def handle_input(self, key):
        if key == 'Q' or key == 'q':
            raise urwid.ExitMainLoop()