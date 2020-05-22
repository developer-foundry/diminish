class ConfigurationOptionsModel():
    """
    ConfigurationOptionsModel contains the lists of available values for the radio button groups
    used by DashboardView to configure the algorithm.
    """

    def __init__(self):
        self.availableModes = ['prerecorded', 'live']
        self.availableAlgorithms = ['crls', 'lms', 'rls']
        self.availableRoles = ['client', 'server']
