import urwid

class VerticalRadioButtonGroup(urwid.GridFlow):
    def __init__(self, name, labelOptions, group, callback, width, hSep, vSep, alignment, model, attribute):
        self.name = name
        self.model = model
        self.attribute = attribute
        urwid.GridFlow.__init__(self, self.build(labelOptions, group, callback, getattr(self.model, self.attribute)), width, hSep, vSep, alignment)
    
    def build(self, labelOptions, group, callback, selectedOption=None):
        self.buttons = []

        for txt in labelOptions:
            r = urwid.RadioButton(group, txt, txt == selectedOption)
            urwid.connect_signal(r, 'change', callback, self.name)
            ra = urwid.AttrWrap(r, 'button normal','button select')
            self.buttons.append(ra)

        return self.buttons
    
    def refresh(self):
        for button in self.buttons:
            if(button.get_label() == getattr(self.model, self.attribute)):
                button.set_state(True)
            else:
                button.set_state(False)
