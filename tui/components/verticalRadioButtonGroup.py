import urwid

class VerticalRadioButtonGroup(urwid.GridFlow):
    def __init__(self, name, labelOptions, group, callback, width, hSep, vSep, alignment, selectedOption=None):
        self.name = name
        urwid.GridFlow.__init__(self, self.build(labelOptions, group, callback, selectedOption), width, hSep, vSep, alignment)
    
    def build(self, labelOptions, group, callback, selectedOption=None):
        buttons = []

        for txt in labelOptions:
            r = urwid.RadioButton(group, txt, txt == selectedOption)
            urwid.connect_signal(r, 'change', callback, self.name)
            ra = urwid.AttrWrap(r, 'button normal','button select')
            buttons.append(ra)

        return buttons