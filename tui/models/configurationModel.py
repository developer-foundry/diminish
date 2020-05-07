class ConfigurationModel():
    mode: ''
    algorithm: ''
    inputFile: ''
    targetFile: ''
    device: ''
    size: 0
    role: ''
    waitSize: 0
    stepSize: 0
    
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