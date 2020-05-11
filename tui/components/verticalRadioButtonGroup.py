import urwid

class VerticalRadioButtonGroup(urwid.GridFlow):
    def __init__(self, model, attribute, labelOptions, group, width, hSep, vSep, alignment):
        self.model = model
        self.attribute = attribute
        urwid.GridFlow.__init__(self, self.build(labelOptions, group, getattr(self.model, self.attribute)), width, hSep, vSep, alignment)
    
    def build(self, labelOptions, group, selectedOption=None):
        self.buttons = []

        for txt in labelOptions:
            r = urwid.RadioButton(group, txt, txt == selectedOption)
            urwid.connect_signal(r, 'change', self.on_radio_change, self.attribute)
            ra = urwid.AttrWrap(r, 'button normal','button select')
            self.buttons.append(ra)

        return self.buttons
    
    def on_radio_change(self, button, state, groupName):
        if state:
            setattr(self.model, self.attribute, button.get_label())

    def refresh(self):
        for button in self.buttons:
            if(button.get_label() == getattr(self.model, self.attribute)):
                button.set_state(True)
            else:
                button.set_state(False)
