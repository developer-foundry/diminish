import urwid

class LoggingView(urwid.WidgetWrap):
    def __init__(self, model, height):
        self.model = model
        self.height = height
        self.entries = urwid.SimpleFocusListWalker(self.convert(self.model.logEntries))
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        return urwid.BoxAdapter(urwid.LineBox(urwid.ListBox(self.entries),title="Logging"), self.height)

    def convert(self, entries):
        textArray = []
        for entry in entries:
            textArray.append(urwid.Text(entry))
        return textArray

    
    def refresh(self):
        self.entries.clear()
        self.entries.extend(self.convert(self.model.logEntries))
