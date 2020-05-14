import urwid

class StatusView(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        self.bigtext = urwid.BigText("", urwid.HalfBlock5x4Font())
        bt = urwid.Padding(self.bigtext, 'center', None)
        self.attribute = urwid.AttrWrap(bt, 'bigtextgood')
        bt = urwid.Filler(self.attribute, 'bottom', None, 7)
        bt = urwid.BoxAdapter(urwid.LineBox(bt, "Status"), 7)

        return bt
    
    def refresh(self):
        state = "On"if not self.model.paused else "Off"
        self.bigtext.set_text(state)

        if(self.model.paused):
            self.attribute.set_attr('bigtextbad')
        else:
            self.attribute.set_attr('bigtextgood')
