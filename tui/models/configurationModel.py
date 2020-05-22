from tui.models.configurationOptionsModel import ConfigurationOptionsModel


class ConfigurationModel():
    """
    ConfigurationModel is the primary model used in the current implementation of diminish
    TUI. The model holds all information that is displayed on the primary screen: DashboardView.
    """

    def __init__(self, parameters):
        """
        Parameters
        ----------
        parameters : array
            An array of environment variables used to initialize the model.
        """
        self.logger = None
        self.mode = parameters['mode']
        self.algorithm = parameters['algorithm']
        self.inputFile = parameters['inputFile']
        self.targetFile = parameters['targetFile']
        self.device = parameters['device']
        self.size = parameters['size']
        self.role = parameters['role']
        self.waitSize = parameters['waitSize']
        self.stepSize = parameters['stepSize']
        self.tuiConnection = parameters['tuiConnection']
        self.graphTop = 0.04
        self.graphBottom = -0.04
        self.logEntries = []
        self.options = ConfigurationOptionsModel()
        self.errorPercentage = 0.0
        self.errorBuffer = []
        self.referenceBuffer = []
        self.outputBuffer = []
        self.memory = 0
        self.cpu = 0
        self.packetsreceived = 0
        self.packetssent = 0
        self.paused = False
