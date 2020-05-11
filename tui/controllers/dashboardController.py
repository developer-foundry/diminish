import urwid
from tui.palette.palette import palette
from tui.views.dashboardView import DashboardView
from tui.models.configurationModel import ConfigurationModel
from random import uniform, randint

class DashboardController():
    def __init__(self, parameters, logger, loggingHandler):
        self.logger = logger
        self.loggingHandler = loggingHandler
        self.model = ConfigurationModel(parameters)
        self.view = DashboardView(self.model)
        self.loop = urwid.MainLoop(self.view, palette=palette, unhandled_input=self.handle_input)

        self.loggingHandler.configureModel(self.model)
    
    def run(self):
        self.loop.set_alarm_in(0, self.refresh)
        self.loop.run()
    
    def refresh(self, _loop, data):
        self.logger.info('Refreshing screen')
        
        self.model.mode = 'prerecorded' if self.model.mode == 'live' else 'live'
        self.model.algorithm = 'rls'
        self.model.errorBuffer.append([uniform(-0.01, 0.01)])
        self.model.referenceBuffer.append([uniform(-0.01, 0.01)])
        self.model.outputBuffer.append([uniform(-0.01, 0.01)])
        self.model.errorPercentage = uniform(0.01, 0.99)
        self.view.refresh()
        _loop.set_alarm_in(1, self.refresh)

    # Handle key presses
    def handle_input(self, key):
        if key == 'Q' or key == 'q':
            raise urwid.ExitMainLoop()