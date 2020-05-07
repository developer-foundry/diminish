import urwid

class RadioButtonGroup(list):
    def __init__(self, labelOptions, group, callback, selectedOption=None):
        for label in labelOptions:
            rb = self.radio_button( group, label, callback, selectedOption)
            self.append( rb )
    
    def radio_button(self, g, l, fn, selectedOption):
        w = urwid.RadioButton(g, l, l == selectedOption, on_state_change=fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w
