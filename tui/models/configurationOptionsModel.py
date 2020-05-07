class ConfigurationOptionsModel():
    def __init__(self):
        self.availableModes = ['prerecorded', 'live']
        self.availableAlgorithms = ['crls', 'lms', 'rls']
        self.availableRoles = ['client', 'server']