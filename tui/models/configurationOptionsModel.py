class ConfigurationOptionsModel():
    def __init__(self):
        self.availableModes = ['prerecorded', 'live']
        self.availableAlgorithm = ['crls', 'lms', 'rls']
        self.availableRoles = ['client', 'server']