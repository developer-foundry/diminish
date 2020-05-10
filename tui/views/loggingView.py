import urwid

class LoggingView(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        self.entries = urwid.SimpleFocusListWalker(self.convert(self.model.logEntries))
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        return urwid.BoxAdapter(urwid.LineBox(urwid.ListBox(self.entries)), 10)

    def convert(self, entries):
        textArray = []
        for entry in entries:
            textArray.append(urwid.Text(entry))
        return textArray

    
    def refresh(self):
        self.entries.clear()
        self.entries.extend(self.convert(self.model.logEntries))
