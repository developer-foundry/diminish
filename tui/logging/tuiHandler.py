from logging import StreamHandler

class TuiHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)
        
    def emit(self, record):
        msg = self.format(record)
        self.model.logEntries.append(msg)

    def configureModel(self, model):
        self.model = model
        self.model.logEntries = []