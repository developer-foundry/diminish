from logging import StreamHandler

class TuiHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)
        
    def emit(self, record):
        if(record.levelno  >= self.level):
            msg = self.format(record)
            msg = msg.replace("\\\'", "'")
            messages = msg.split("\\n")
            for message in messages:
                if(message != '"' and message != "'"):
                    self.model.logEntries.append(message)

    def configureModel(self, model):
        self.model = model
        self.model.logEntries = []