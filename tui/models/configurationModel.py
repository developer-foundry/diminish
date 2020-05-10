from tui.models.configurationOptionsModel import ConfigurationOptionsModel

class ConfigurationModel():
    def __init__(self, parameters):
        self.mode = parameters['mode']
        self.algorithm = parameters['algorithm']
        self.inputFile = parameters['inputFile']
        self.targetFile = parameters['targetFile']
        self.device = parameters['device']
        self.size = parameters['size']
        self.role = parameters['role']
        self.waitSize = parameters['waitSize']
        self.stepSize = parameters['stepSize']
        self.errorBuffer = [ [0.005], [-0.005], [0.005], [-0.005], [0.005], [-0.005], [0.005], [-0.005], [0.005], [-0.005], [0.005], [-0.005], [0.005], [-0.005]]
        self.graphTop = 0.01
        self.graphBottom = -0.01
        self.options = ConfigurationOptionsModel()