import urwid
from tui.components.headerComponent import HeaderComponent
from tui.components.verticalRadioButtonGroup import VerticalRadioButtonGroup
import logging

class DashboardControls(urwid.WidgetWrap):
    def __init__(self, model):
        self.model = model
        urwid.WidgetWrap.__init__(self, self.build())
    
    def build(self):
        mode_buttons = VerticalRadioButtonGroup('mode', self.model.options.availableModes, [], self.on_radio_change, 30, 0, 1, 'left', self.model.mode)
        algorithm_buttons = VerticalRadioButtonGroup('algorithm', self.model.options.availableAlgorithms, [], self.on_radio_change, 30, 0, 1, 'left', self.model.algorithm)
        header = HeaderComponent(f'Algorithm Controls', 'header')

        l = [
            header,
            urwid.AttrWrap(urwid.Text("Mode"), 'contentheader'),
            mode_buttons,
            urwid.Divider(),
            urwid.Text("Algorithm"),
            algorithm_buttons,
            ]

        w = urwid.Filler(urwid.Pile(l), 'top')
        return w
    
    def on_radio_change(self, button, state, groupName):
        if state:
            setattr(self.model, groupName, button.get_label())