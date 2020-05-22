from logging import StreamHandler


class TuiHandler(StreamHandler):
    """
    TuiHandler is a custom logging handler that will add log messages
    to a ConfigurationModel object rather than directing the messages
    to stdout or stderr. This prevents urwid from displaying random
    error messages on top of DashboardView.
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        StreamHandler.__init__(self)

    def emit(self, record):
        """
        Called when a message is sent to a logger.

        Parameters
        ----------
        record : LogRecord
            The record passed from the logger that contains the message and log level.

        Returns
        -------
        None

        Raises
        ------
        None
        """
        if(record.levelno >= self.level):
            msg = self.format(record)
            msg = msg.replace("\\\'", "'")
            messages = msg.split("\\n")
            for message in messages:
                if(message != '"' and message != "'"):
                    self.model.logEntries.append(message)

    def configureModel(self, model):
        """
        Called to register the model with the handler so that messages can be appended to logEntries

        Parameters
        ----------
        model : ConfigurationModel
            The model that this component is linked to.

        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.model = model
        self.model.logEntries = []
