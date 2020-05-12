import urwid
import time

class RunningTime(urwid.WidgetWrap):
    def __init__(self):
        self.startTime = time.time()
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        self.bigtext = urwid.BigText("", urwid.HalfBlock5x4Font())
        bt = urwid.Padding(self.bigtext, 'center', None)
        self.attribute = urwid.AttrWrap(bt, 'bigtextgood')
        bt = urwid.Filler(self.attribute, 'bottom', None, 7)
        bt = urwid.BoxAdapter(urwid.LineBox(bt, "Running Time (s)"), 7)

        return bt
    
    def refresh(self):
        timePassed = f"{int(time.time() - self.startTime)}"
        self.bigtext.set_text(timePassed)
