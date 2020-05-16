import urwid

class ErrorPercentage(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())

    def build(self):
        self.bigtext = urwid.BigText("", urwid.HalfBlock5x4Font())
        bt = urwid.Padding(self.bigtext, 'center', None)
        self.attribute = urwid.AttrWrap(bt, 'bigtextgood')
        bt = urwid.Filler(self.attribute, 'bottom', None, 7)
        bt = urwid.BoxAdapter(urwid.LineBox(bt, "Error Rate"), 7)

        return bt
    
    def refresh(self):
        percentage = "{0:1.3f}".format(self.model.errorPercentage)
        self.bigtext.set_text(percentage)

        if(self.model.errorPercentage >= 0.001):
            self.attribute.set_attr('bigtextbad')
        else:
            self.attribute.set_attr('bigtextgood')
